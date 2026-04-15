---
name: calibracion-datos-reales
description: Every system output must be compared against at least 1 real-world case. If the output is out of real range, there is a bug. Applies to any computation engine, ML model, or simulation.
type: feedback
---
# Real Data Calibration

## Applies to: Any system that produces numerical or measurable outputs (computation engines, ML, simulations, analytics)

## Rule
Each new module -> compare output with at least 1 REAL documented case.

## Example reference ranges (adapt to your domain):
- API response time: 50-500ms (real benchmark: 120ms)
- Compression ratio: 2x-10x (real test: 4.3x)
- ML model accuracy: domain-dependent (published baseline: 0.87)
- Cost estimate: within 20% of known reference

## Protocol
1. Identify a comparable real case (project, paper, benchmark, database)
2. Run the system with the SAME inputs as the real case
3. Compare output vs real: within acceptable tolerance (e.g., +/-20%)?
4. If out of range -> investigate the cause before continuing

## Anti-pattern: the Impossible Ratio
```
BAD: "output value = 50" (without comparing) -> turns out real-world is 350 (7x off)
GOOD: "Reference case = 252, our system gives 253 -> OK (0.4% error)"
```

**Why:** Output values were 7x lower than real-world references due to an incorrect fallback.
**How to apply:** Before delivering output -> is it in real-world range? If not -> bug.
