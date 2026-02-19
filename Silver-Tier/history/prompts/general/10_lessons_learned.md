# Prompt: lessons_learned
## Date: 2026-02-19
## Purpose: Document key lessons, errors faced, and fixes during Silver Tier development

## Prompt Used:
Document the lessons learned during Silver Tier development including:
- Technical challenges encountered
- Errors and their resolutions
- Design decisions and rationale
- Best practices discovered
- Gotchas and workarounds

## Result:
Created this lessons learned document capturing development experience.

## Notes:

### Key Lessons Learned

#### 1. Path Handling with Spaces
**Problem:** Windows paths with spaces ("MUDASIR SOHAIL", "Hackathon 0") broke schtasks commands.
**Solution:** Escape quotes in command strings: `f'\\"{PYTHON_EXE}\\" \\"{script_path}\\"'`
**Lesson:** Always test with spaces in paths; use escaped quotes for Windows Task Scheduler.

#### 2. WhatsApp Web Selector Stability
**Problem:** WhatsApp Web changes CSS selectors frequently, breaking DOM-based scraping.
**Solution:** Use JavaScript evaluation to extract chat text directly from sidebar (#pane-side) rather than relying on specific class names.
**Lesson:** JavaScript evaluation is more resilient than CSS selector chains for dynamic web apps.

#### 3. Filesystem-Safe Filenames
**Problem:** Sender names with special characters (/, \, :) caused file creation errors.
**Solution:** Sanitize filenames: `replace(" ", "_").replace("/", "-").replace("\\", "-").replace(":", "")`
**Lesson:** Always sanitize user-generated content before using in file paths.

#### 4. Session Persistence
**Problem:** Browser automation required QR code scan every run.
**Solution:** Use persistent context with saved session directories.
**Lesson:** Playwright's launch_persistent_context() maintains login state across runs.

#### 5. Deduplication Strategy
**Problem:** Same messages processed multiple times.
**Solution:** Fingerprint-based deduplication: `f"{sender}:{text[:50]}"`
**Lesson:** Content-based fingerprints prevent duplicate processing without database.

#### 6. Modular Watcher Design
**Decision:** BaseWatcher class with check_for_updates() and create_action_file() interface.
**Benefit:** Easy to add new watchers (Slack, Teams, etc.) by inheritance.
**Lesson:** Interface-based design enables extensibility.

#### 7. Approval Handler Timing
**Decision:** Approval handler runs every 30 seconds, watchers every 2 minutes.
**Rationale:** Faster approval cycle improves user experience.
**Lesson:** Different components need different polling intervals based on use case.

#### 8. Credential Management
**Decision:** PersonalAI_Vault/credentials/ folder with JSON files.
**Rationale:** Centralized, version-controllable (with .gitignore) credential storage.
**Lesson:** Separate credentials from code; use .gitignore religiously.

### Best Practices Established

1. **Never hardcode secrets** - Use .env or credential files
2. **Log everything** - Each watcher has its own log file
3. **Small, testable methods** - check_for_updates(), create_action_file()
4. **Graceful degradation** - Return empty list on errors, don't crash
5. **Document as you go** - PHR files capture decisions

### Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| schtasks fails with error 0x1 | Path with spaces not escaped | Use `\\"` for nested quotes |
| WhatsApp requires QR every time | Session not persisted | Use persistent_context with session_path |
| File creation fails | Special chars in filename | Sanitize with replace() |
| Gmail API auth fails | Credentials file missing | Check PersonalAI_Vault/credentials/ |
| Selectors not found | WhatsApp Web UI changed | Use JavaScript evaluation |

### Future Improvements

1. Add webhook support instead of polling
2. Implement retry logic with exponential backoff
3. Add metrics/monitoring dashboard
4. Support for multiple WhatsApp accounts
5. Email threading for Gmail conversations
