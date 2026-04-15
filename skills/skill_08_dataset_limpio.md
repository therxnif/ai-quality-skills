---
name: dataset-limpio
description: Cada corrección al motor invalida el dataset existente. Regenerar COMPLETO antes de reentrenar ML. No mezclar datos viejos con nuevos.
type: feedback
originSessionId: a0d34ba2-2a13-421f-b624-f0f12c1a7219
---
# Dataset Limpio

## Aplica a: Cualquier sistema con ML entrenado sobre datos generados por el propio sistema

## Regla
Si el motor cambia → el dataset generado con el motor viejo es BASURA.

## Protocolo
```
Motor corregido (30 fixes)
  → Dataset viejo (24,700 casos) = CONTAMINADO
  → Regenerar COMPLETO con motor nuevo
  → Verificar que nuevos datos son consistentes (sample 100 casos)
  → Reentrenar ML
  → Verificar R² con datos NUEVOS (no viejos)
```

## Anti-patrón: el Dataset Frankenstein
```
MAL: "Agrego 10K casos nuevos al dataset existente"
     → Mezcla datos con Whitney+beta1 (viejo) y sin beta1 (nuevo)
     → ML aprende patrones INCONSISTENTES
BIEN: Regenerar TODO desde cero con motor corregido
```

## Señales de dataset contaminado
- Campos reutilizados (FSD_volteo = eta_grupo)
- Valores de checks del módulo equivocado
- R² sube sin motivo aparente
- Predicciones contradicen la ingeniería

**Why:** 24,700 casos con fórmulas incorrectas usados para entrenar ML.
**How to apply:** Después de CADA corrección al motor → flag dataset como inválido.
