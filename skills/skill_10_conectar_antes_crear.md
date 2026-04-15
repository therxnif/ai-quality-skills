---
name: conectar-antes-de-crear
description: No crear features nuevas hasta que las existentes estén CONECTADAS al pipeline y verificadas. 1 feature conectada > 10 features sueltas.
type: feedback
originSessionId: a0d34ba2-2a13-421f-b624-f0f12c1a7219
---
# Conectar Antes de Crear

## Aplica a: Cualquier proyecto con múltiples módulos/features

## Regla
Antes de crear algo nuevo, verificar:
1. ¿Las features existentes están CONECTADAS al pipeline?
2. ¿Se pueden usar desde el endpoint/UI?
3. ¿Tienen tests?
4. ¿Están documentadas?

Si la respuesta es NO → CONECTAR primero, crear después.

## Anti-patrón: el Módulo Fantasma
```
MAL: "Sesión 44: construí 24 módulos nuevos (Intelligence Engine, KG, RL, CO2...)"
     → Ninguno conectado al pipeline
     → El usuario no puede usarlos
     → Dan falsa sensación de progreso
BIEN: "Conecté CO2 al disenar_puente(). Ahora cada puente tiene huella de carbono."
     → 1 feature REAL en producción
```

## Métrica de progreso real
```
FALSO progreso: "140K líneas de código, 24 módulos"
REAL progreso: "7 tipologías funcionan end-to-end, 100 memorias generadas correctamente"
```

## Checklist antes de crear algo nuevo
- [ ] ¿Lo existente funciona end-to-end?
- [ ] ¿Hay features desconectadas que debería conectar primero?
- [ ] ¿El usuario puede usar la feature desde la UI/API?
- [ ] ¿Tiene tests que corren?
- [ ] ¿Está en el deploy de producción?

**Why:** 24 módulos construidos, 0 conectados. Prioridad absoluta era CONECTAR.
**How to apply:** Preguntar "¿está conectado?" antes de crear. Si no → conectar primero.
