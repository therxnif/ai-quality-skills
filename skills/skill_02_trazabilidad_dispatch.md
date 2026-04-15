---
name: trazabilidad-dispatch
description: Antes de auditar cualquier módulo, verificar que ESE módulo se ejecuta realmente. Trazar routing/dispatch completo. Aplica a cualquier sistema con routing, dispatch, factory, strategy pattern.
type: feedback
originSessionId: a0d34ba2-2a13-421f-b624-f0f12c1a7219
---
# Trazabilidad de Dispatch

## Aplica a: Cualquier sistema con routing (API endpoints, module dispatch, factory pattern, strategy)

## Protocolo
1. Identificar el punto de dispatch (router, factory, dict lookup, if/elif chain)
2. Verificar case sensitivity (`.lower()`, `.upper()`, exact match)
3. Verificar default/fallback (¿qué pasa si no matchea?)
4. TRAZAR con print/log: input → dispatch → módulo real ejecutado
5. Si hay default → SOSPECHAR. El default puede enmascarar bugs.

## Checklist
- [ ] ¿El dispatch normaliza el input? (case, trim, encoding)
- [ ] ¿El default es seguro o enmascara errores?
- [ ] ¿Tracé qué módulo realmente se ejecutó? (no asumí)
- [ ] ¿Los tests cubren TODOS los valores de dispatch? (no solo el happy path)

## Anti-patrón: el Default Silencioso
```python
# PELIGROSO: si tipologia="T07" y dict tiene "t07", cae al default
modulo = MODULOS.get(tipologia, modulo_default)
# SEGURO:
modulo = MODULOS.get(tipologia.lower(), None)
if modulo is None: raise ValueError(f"Tipología desconocida: {tipologia}")
```

**Why:** `.lower()` faltante hizo que T07 usara módulo RC por 36 sesiones.
**How to apply:** En CADA sistema con dispatch, trazar antes de confiar.
