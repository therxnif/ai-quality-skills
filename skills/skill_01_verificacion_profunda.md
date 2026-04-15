---
name: verificacion-profunda
description: OBLIGATORIO antes de reportar resultados o decir que algo funciona. Aplica a TODO proyecto — SaaS, API, motor de cálculo, frontend, deploy.
type: feedback
originSessionId: a0d34ba2-2a13-421f-b624-f0f12c1a7219
---
# Verificación Profunda

## Aplica a: CUALQUIER proyecto de software

## 10 Reglas

1. NUNCA reportar sin ejecutar el código real
2. NUNCA asumir que el módulo/ruta/dispatch correcto se ejecuta — TRAZAR
3. NUNCA aceptar tests PASS sin verificar que los valores son reales (no hardcoded)
4. NUNCA reportar score/porcentaje sin verificar el denominador
5. Cada fix debe probarse con el CASO EXACTO que fallaba
6. Cada valor numérico debe tener sentido (comparar con referencia real)
7. NUNCA clasificar un fail como "conocido" — investigar y resolver
8. Frontend = verificar visualmente en navegador, no solo build
9. Deploy = curl al endpoint real en producción
10. Reportes/docs = abrir y leer, no solo contar tamaño

## Frases PROHIBIDAS sin verificar
"funciona", "100%", "0 errores", "issue conocido", "debería funcionar", "ya se fixeó", "todo actualizado", "deploy exitoso"

**Why:** 45 sesiones reportando éxito falso por verificación superficial.
**How to apply:** Ejecutar checklist COMPLETO antes de cada claim. Sin excepciones.
