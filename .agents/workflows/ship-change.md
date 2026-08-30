# Workflow: Ship Change (`/ship-change`)

Follow this standardized procedure for any production change or maintenance update:

1. **Lint & Type Check**:
   - Backend: Ensure Python types and syntax pass clean.
   - Frontend: Run `npm run lint` or `npx tsc --noEmit`.

2. **Run Automated Test Suite**:
   - Execute `pytest backend/tests/` and verify 100% pass rate.

3. **Verify in Live Browser**:
   - Launch local servers.
   - Run Browser Subagent to check the affected user flow (e.g. analysis, history, chat).
   - Ensure no console errors or visual regressions.

4. **Update Memory if Conventions Changed**:
   - If a new environment variable or architectural pattern was added, update `AGENTS.md` and the relevant `.agents/rules/*.md` file.

5. **Commit**:
   - Create clean conventional commit: `git commit -m "type(scope): description"`
