---
name: auto-ajuste-completo
description: Every auto-adjustment must verify ALL constraints after each change, not just the one that triggered it. If improving A worsens B, iterate until equilibrium.
type: feedback
---
# Complete Auto-Adjust

## Applies to: Any system with iterative optimization, auto-sizing, auto-correction, or constraint satisfaction

## Rule
Adjusting ONE parameter can violate ANOTHER constraint. The loop must verify ALL.

## Anti-pattern: the Fix that Breaks
```
BAD: "Auto-fix: if memory > limit -> reduce cache size"
     -> But never checks: does throughput still meet SLA? Is latency acceptable?
GOOD: Reduce cache -> re-verify: memory, throughput, latency, error rate, cost
```

## Protocol
1. Identify ALL constraints of the component
2. The loop adjusts the parameter AND re-verifies ALL constraints
3. Maximum 10 iterations with logging
4. If it doesn't converge -> flag "requires manual intervention" (don't force it)
5. Record state before/after each iteration

## Checklist
- [ ] The auto-adjust verifies ALL constraints, not just the trigger
- [ ] There is an iteration limit (no infinite loops)
- [ ] If conflict (A wants more, B wants less) -> escalate to a different parameter
- [ ] If it doesn't converge -> clear message, don't force ok=True

**Why:** Auto-fix only addressed one constraint while breaking others — went undetected for weeks.
**How to apply:** Each adjustment loop -> re-verify EVERYTHING after each step.
