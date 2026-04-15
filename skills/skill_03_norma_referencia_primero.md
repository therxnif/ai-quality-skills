---
name: norma-referencia-primero
description: Before adding any check, validation, or formula — read the official spec/standard/docs. Do not invent. Do not copy from another module without verifying it applies.
type: feedback
---
# Standard/Reference First

## Applies to: Any system that implements standards, specs, or documented rules (RFCs, ISO, OWASP, W3C, language specs, API docs, etc.)

## Rule
Before writing ONE line of code that implements a rule:
1. What spec/standard does it come from? (exact section)
2. Does it apply to THIS type of component? (different types have different rules)
3. Is the formula correct in the system's units/types?
4. Are there applicability conditions? (only for X, not for Y)

## Anti-pattern: the Normative Copy-Paste
```
BAD: "I'll add this validation to all handlers"
     -> The rule from one domain doesn't apply to another
GOOD: "What spec applies to THIS specific type? -> Section 4.2: different limit"
```

## Checklist
- [ ] I cited the exact section of the spec/standard
- [ ] I verified it applies to THIS type of component
- [ ] The units/types are correct
- [ ] The applicability conditions are met

**Why:** Rules from one domain were applied to another for 10+ sessions without anyone noticing.
**How to apply:** READ the spec section before coding. Never copy from another module blindly.
