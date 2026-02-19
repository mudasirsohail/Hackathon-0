# Prompt: constitution
## Date: 2026-02-19
## Purpose: Create the project constitution (sp.constitution.md) defining code quality, testing, performance, security, and architecture principles for Silver Tier

## Prompt Used:
Create a constitution document for a Personal AI Assistant Silver Tier project. This is a Windows-based system that monitors Gmail, WhatsApp Web, handles approvals, and posts to LinkedIn.

The constitution should define:
1. Code Quality Standards (naming, structure, documentation)
2. Testing Principles (unit tests, integration tests, error handling)
3. Performance Requirements (response times, resource limits)
4. Security Principles (credential handling, session management, API keys)
5. Architecture Principles (modularity, separation of concerns, logging)

This project uses Python with Playwright for browser automation, Google API for Gmail, and runs on Windows Task Scheduler.

## Result:
Created `.specify/memory/constitution.md` with comprehensive project principles covering:
- Python naming conventions (PascalCase for classes, snake_case for functions)
- Mandatory error handling with try-except blocks and logging
- Security requirements for credential storage (no hardcoded secrets)
- Session persistence for browser automation
- Modular architecture with base watcher class inheritance
- Windows Task Scheduler integration requirements

## Notes:
- Constitution serves as the authoritative source for all coding decisions
- All subsequent files (SPEC.md, PLAN.md, TASKS.md) must align with these principles
- Security emphasis on `.env` files and credential vaults for sensitive data
