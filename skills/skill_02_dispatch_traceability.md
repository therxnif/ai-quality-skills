---
name: trazabilidad-dispatch
description: Before auditing any module, verify that THAT module actually executes. Trace routing/dispatch completely. Applies to any system with routing, dispatch, factory, or strategy pattern.
type: feedback
---
# Dispatch Traceability

## Applies to: Any system with routing (API endpoints, module dispatch, factory pattern, strategy)

## Protocol
1. Identify the dispatch point (router, factory, dict lookup, if/elif chain)
2. Verify case sensitivity (`.lower()`, `.upper()`, exact match)
3. Verify default/fallback (what happens if nothing matches?)
4. TRACE with print/log: input -> dispatch -> actual module executed
5. If there's a default -> SUSPECT IT. The default can mask bugs.

## Checklist
- [ ] Does the dispatch normalize the input? (case, trim, encoding)
- [ ] Is the default safe, or does it mask errors?
- [ ] Did I trace which module actually executed? (not assumed)
- [ ] Do the tests cover ALL dispatch values? (not just the happy path)

## Anti-pattern: the Silent Default
```python
# DANGEROUS: if key="TypeB" and dict has "typeb", falls to default
handler = HANDLERS.get(key, default_handler)
# SAFE:
handler = HANDLERS.get(key.lower(), None)
if handler is None: raise ValueError(f"Unknown type: {key}")
```

**Why:** A missing `.lower()` caused the wrong module to run silently for 36 sessions.
**How to apply:** In EVERY system with dispatch, trace before trusting.
