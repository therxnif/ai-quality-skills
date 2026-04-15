---
name: propagacion-instantanea
description: Each change to the core/engine must propagate INSTANTLY to all consumers (UI, reports, validators, frontend, docs, datasets). Do not leave for later.
type: feedback
---
# Instant Propagation

## Applies to: Any system with multiple layers that consume data from a core

## Rule
When you change the core/engine, these are IMMEDIATELY invalidated:
1. Frontend (tabs, charts, tables)
2. Reports/documents (sections, values, checks)
3. Independent validators (must stay consistent)
4. ML datasets (data generated with old engine = contaminated)
5. Documentation (formulas, result tables)
6. Tests (assertions with old values)

## Protocol
```
Change in core
  -> List affected consumers (grep imports, grep function name)
  -> For EACH consumer: does it show the new data? Does it use the correct field?
  -> Update INSTANTLY (not "in the next session")
  -> Verify that the full pipeline works end-to-end
```

## Anti-pattern: the "I'll Update It Later"
```
BAD: "Core fixed, I'll update the frontend later"
     -> 5 sessions later: frontend still shows old data
GOOD: Core fixed -> frontend + reports + validator in the SAME commit
```

**Why:** Core had 30 corrections but frontend/reports/docs stayed outdated for the entire session.
**How to apply:** Each change to the core -> propagate to ALL consumers before committing.
