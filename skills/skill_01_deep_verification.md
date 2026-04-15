---
name: verificacion-profunda
description: MANDATORY before reporting results or claiming something works. Applies to ANY software project — web apps, APIs, ML, games, mobile, CLI tools.
type: feedback
---
# Deep Verification

## Applies to: ANY software project

## 10 Rules

1. NEVER report without running the actual code
2. NEVER assume the correct module/route/dispatch executed — TRACE it
3. NEVER accept tests PASS without verifying values are real (not hardcoded)
4. NEVER report score/percentage without verifying the denominator
5. Each fix must be tested with the EXACT CASE that was failing
6. Each numerical value must make sense (compare with real-world reference)
7. NEVER classify a fail as "known" — investigate and resolve
8. Frontend = verify visually in the browser, not just build
9. Deploy = curl the real endpoint in production
10. Reports/docs = open and read, not just check file size

## BANNED phrases without verification
"works", "100%", "0 errors", "known issue", "should work", "already fixed", "all updated", "deploy successful"

**Why:** 45+ sessions of reporting false success due to shallow verification.
**How to apply:** Run the COMPLETE checklist before each claim. No exceptions.
