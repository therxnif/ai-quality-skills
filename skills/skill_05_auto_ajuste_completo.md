---
name: auto-ajuste-completo
description: Todo auto-ajuste debe verificar TODAS las restricciones después de cada ajuste, no solo la que disparó. Si mejorar A empeora B → iterar hasta equilibrio.
type: feedback
originSessionId: a0d34ba2-2a13-421f-b624-f0f12c1a7219
---
# Auto-Ajuste Completo

## Aplica a: Cualquier sistema con optimización iterativa, auto-sizing, auto-correction

## Regla
Ajustar UN parámetro puede violar OTRO check. El loop debe verificar TODO.

## Anti-patrón: el Fix que Rompe
```
MAL: "Auto-ajuste pilotes: si Q < P → agregar 1 pilote"
     → Pero nunca chequea: ¿el encepado cabe? ¿la separación es ≥ 3D?
BIEN: Agregar pilote → re-verificar: axial, lateral, separación, encepado, costo
```

## Protocolo
1. Identificar TODAS las restricciones del componente
2. El loop ajusta el parámetro Y re-verifica TODAS
3. Máximo 10 iteraciones con logging
4. Si no converge → flag "requiere diseño manual" (no forzar)
5. Registrar estado antes/después de cada iteración

## Checklist
- [ ] El auto-ajuste verifica TODAS las restricciones, no solo la trigger
- [ ] Hay límite de iteraciones (no loop infinito)
- [ ] Si conflicto (A quiere más, B quiere menos) → escalar parámetro diferente
- [ ] Si no converge → mensaje claro, no forzar ok=True

**Why:** Pilotes solo sumaba cantidad (no D, L). Debonding solo chequeaba bottom (no top).
**How to apply:** Cada loop de ajuste → re-verificar TODO después de cada paso.
