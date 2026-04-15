---
name: propagacion-instantanea
description: Cada cambio al motor/core debe propagarse AL INSTANTE a todos los consumidores (GUI, memoria, verificador, frontend, papers, dataset). No dejar para después.
type: feedback
originSessionId: a0d34ba2-2a13-421f-b624-f0f12c1a7219
---
# Propagación Instantánea

## Aplica a: Cualquier sistema con múltiples capas que consumen datos de un core

## Regla
Cuando cambias el core/motor, estos se invalidan INMEDIATAMENTE:
1. Frontend (tabs, gráficos, tablas)
2. Memoria/reportes (secciones, valores, checks)
3. Verificador independiente (debe ser consistente)
4. Dataset ML (datos generados con motor viejo = contaminados)
5. Papers (fórmulas, tablas de resultados)
6. Tests (assertions con valores viejos)

## Protocolo
```
Cambio en motor
  → Lista de afectados (grep imports, grep function name)
  → Para CADA afectado: ¿muestra el dato nuevo? ¿usa el campo correcto?
  → Actualizar AL INSTANTE (no "en la próxima sesión")
  → Verificar que el pipeline completo funciona end-to-end
```

## Anti-patrón: el "Después lo actualizo"
```
MAL: "Motor corregido, frontend lo actualizo después"
     → 5 sesiones después: frontend sigue mostrando datos viejos
BIEN: Motor corregido → frontend + memoria + verificador en el MISMO commit
```

**Why:** Motor con 30 correcciones pero frontend/memoria/papers desactualizados durante toda la sesión.
**How to apply:** Cada cambio al core → propagar a TODOS los consumidores antes de commitear.
