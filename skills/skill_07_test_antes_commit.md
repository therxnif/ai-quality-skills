---
name: test-antes-de-commit
description: Before each commit — verify syntax, imports, and at least 1 real execution case. Never commit code that doesn't compile or run.
type: feedback
---
# Test Before Commit

## Applies to: ANY software project

## Pre-commit protocol
```bash
# 1. Syntax check of each modified file
python -c "import ast; ast.parse(open('file.py').read())"
# Or for JS/TS: npx tsc --noEmit
# Or for Rust: cargo check

# 2. Import check
python -c "from module import function"
# Or: node -e "require('./module')"

# 3. Smoke test (at least 1 real execution)
python -c "from app import main; main(minimal_inputs)"
# Or: npm test -- --bail

# 4. If there's an endpoint: real curl
curl -s http://localhost:8000/endpoint
```

## Anti-pattern: the "Commit and Pray"
```
BAD: git commit -> deploy -> 500 Internal Server Error
GOOD: syntax OK -> import OK -> smoke test OK -> commit -> deploy -> curl OK
```

## Checklist
- [ ] Syntax check of each modified file
- [ ] Import/require of each modified module
- [ ] At least 1 real case executed without error
- [ ] If there are endpoints: tested with curl
- [ ] If there's frontend: build completes without errors

**Why:** Commits with UnboundLocalError, undefined variables, syntax errors reached production.
**How to apply:** ALWAYS before `git commit`. No exceptions.
