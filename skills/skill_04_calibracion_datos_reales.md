---
name: calibracion-datos-reales
description: Todo output del sistema debe compararse contra al menos 1 caso real. Si el output no está en rango real → hay un bug. Aplica a cualquier motor de cálculo, ML, simulación.
type: feedback
originSessionId: a0d34ba2-2a13-421f-b624-f0f12c1a7219
---
# Calibración contra Datos Reales

## Aplica a: Cualquier sistema que produce valores numéricos (motores de cálculo, ML, simulaciones)

## Regla
Cada módulo nuevo → comparar output con al menos 1 caso REAL documentado.

## Rangos de referencia (ejemplo puentes):
- Acero kg/m³ concreto: 150-350 (Amazonas real: 252)
- Costo/m² tablero: $800-3000 (PROVIAS real: $1,500-2,500)
- Drift sísmico: 0.1%-2.5%
- Período fundamental: 0.3-3.0s

## Protocolo
1. Identificar caso real comparable (proyecto, paper, base de datos)
2. Correr el sistema con los MISMOS inputs del caso real
3. Comparar output vs real: ¿dentro de ±20%?
4. Si fuera de rango → investigar la causa antes de continuar

## Anti-patrón: el Ratio Imposible
```
MAL: "metrado acero = 50 kg/m³" (sin comparar) → rho=0.004 vs real 0.031
BIEN: "Amazonas real = 252 kg/m³, motor da 253 → OK (0.4% error)"
```

**Why:** Metrado de acero con factor 7x bajo por fallback incorrecto.
**How to apply:** Antes de entregar output → ¿está en rango real? Si no → bug.
