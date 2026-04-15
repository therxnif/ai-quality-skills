---
name: reporte-como-auditor
description: Every generated report/document must be an AUDITOR of the engine, not its echo. If the report says OK but the value fails the check, that is a bug in the report.
type: feedback
---
# Report as Auditor

## Applies to: Any system that generates documents/reports from computed data

## Rule
The report is NOT a "pretty print" of the engine. It is an INDEPENDENT AUDITOR.

## Protocol
```
Engine produces: value=30303, limit=34748, ok=True
Report must:
  1. Show the value (30,303)
  2. Show the limit (34,748)
  3. Cite the source rule (Spec Section 5.6.3)
  4. Verify independently: 30,303 <= 34,748 -> OK
  5. NOT invent formulas — ZERO calculations in the report
  6. If the engine says ok=True but value > limit -> REPORT as a bug
```

## Anti-pattern: the Accomplice Report
```
BAD: Engine says ok=True -> report shows green checkmark without verifying
     -> Engine has ok=True hardcoded -> report covers up the bug
GOOD: Report reads value AND limit, checks value <= limit, THEN shows green/red
```

## Checklist for each report section
- [ ] Does the value come from the engine? (not recalculated)
- [ ] Is the limit correct for this rule/spec?
- [ ] Is the status indicator consistent with value vs limit?
- [ ] Is the reference correct for this component type?
- [ ] Does the section actually exist in the generated output? (grep, don't assume)

**Why:** Reports with 194 checks showing "PASS" — all from the wrong module's data.
**How to apply:** Generate report -> OPEN IT -> verify that each section is correct.
