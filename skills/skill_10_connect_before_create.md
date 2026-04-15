---
name: conectar-antes-de-crear
description: Do not create new features until existing ones are CONNECTED to the pipeline and verified. 1 connected feature > 10 disconnected features.
type: feedback
---
# Connect Before Create

## Applies to: Any project with multiple modules/features

## Rule
Before creating something new, verify:
1. Are existing features CONNECTED to the pipeline?
2. Can they be used from the endpoint/UI?
3. Do they have tests?
4. Are they documented?

If the answer is NO -> CONNECT first, create later.

## Anti-pattern: the Phantom Module
```
BAD: "Built 24 new features (analytics engine, knowledge graph, RL optimizer...)"
     -> None connected to the pipeline
     -> Users can't access any of them
     -> Gives a false sense of progress
GOOD: "Connected the analytics module to the main API. Users now get insights on every request."
     -> 1 REAL feature in production
```

## Metric of real progress
```
FALSE progress: "140K lines of code, 24 modules"
REAL progress: "7 features work end-to-end, 100 reports generated correctly"
```

## Checklist before creating something new
- [ ] Does what exists work end-to-end?
- [ ] Are there disconnected features that should be connected first?
- [ ] Can the user access the feature from the UI/API?
- [ ] Does it have tests that run?
- [ ] Is it in the production deploy?

**Why:** 24 features built, 0 connected to the pipeline. Absolute priority was to CONNECT.
**How to apply:** Ask "is it connected?" before creating. If not -> connect first.
