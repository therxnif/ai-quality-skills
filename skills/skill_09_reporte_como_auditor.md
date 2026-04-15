---
name: reporte-como-auditor
description: Todo reporte/memoria/documento generado debe ser un AUDITOR del motor, no su eco. Si el reporte dice OK pero el valor no cumple → bug en el reporte.
type: feedback
originSessionId: a0d34ba2-2a13-421f-b624-f0f12c1a7219
---
# Reporte como Auditor

## Aplica a: Cualquier sistema que genera documentos/reportes a partir de cálculos

## Regla
El reporte NO es un "pretty print" del motor. Es un AUDITOR INDEPENDIENTE.

## Protocolo
```
Motor produce: valor=30,303, limite=34,748, ok=True
Reporte debe:
  1. Mostrar el valor (30,303)
  2. Mostrar el límite (34,748)
  3. Citar la norma (AASHTO §5.6.3.2)
  4. Verificar independientemente: 30,303 ≤ 34,748 → OK
  5. NO inventar fórmulas — ZERO cálculos en el reporte
  6. Si el motor dice ok=True pero valor > limite → REPORTAR como bug
```

## Anti-patrón: el Reporte Cómplice
```
MAL: Motor dice ok=True → reporte muestra semáforo verde sin verificar
     → Motor tiene ok=True hardcoded → reporte encubre el bug
BIEN: Reporte lee valor Y limite, calcula valor ≤ limite, LUEGO pone verde/rojo
```

## Checklist para cada sección del reporte
- [ ] ¿El valor viene del motor? (no recalculado)
- [ ] ¿El límite es correcto para esta norma?
- [ ] ¿El semáforo es consistente con valor vs límite?
- [ ] ¿La referencia normativa es correcta para este tipo de estructura?
- [ ] ¿La sección existe en el HTML generado? (grep, no asumir)

**Why:** Memorias con 194 checks "PASS" del módulo equivocado.
**How to apply:** Generar reporte → ABRIRLO → verificar que cada sección es correcta.
