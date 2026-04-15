---
name: norma-referencia-primero
description: Antes de agregar cualquier check, validación o fórmula — leer la norma/spec/docs oficial. No inventar. No copiar de otro módulo sin verificar que aplica.
type: feedback
originSessionId: a0d34ba2-2a13-421f-b624-f0f12c1a7219
---
# Norma/Referencia Primero

## Aplica a: Cualquier sistema que implementa estándares (AASHTO, ISO, OWASP, RFC, etc.)

## Regla
Antes de escribir UNA línea de código que implementa una regla:
1. ¿De qué norma/spec viene? (artículo exacto)
2. ¿Aplica a ESTE tipo de componente? (RC ≠ acero ≠ PS)
3. ¿La fórmula es correcta en las unidades del sistema? (SI vs imperial)
4. ¿Hay condiciones de aplicabilidad? (solo para X, no para Y)

## Anti-patrón: el Copy-Paste Normativo
```
MAL: "Voy a agregar h/bw ≤ 6 a todos los cajones"
     → §5.7.2 es para RC, no aplica a acero §6.11
BIEN: "¿Qué artículo aplica a cajón METÁLICO? → §6.10.2: D/tw ≤ 150"
```

## Checklist
- [ ] Cité el artículo exacto de la norma
- [ ] Verifiqué que aplica a ESTE tipo de componente
- [ ] Las unidades son correctas (MPa no ksi, m no ft)
- [ ] Las condiciones de aplicabilidad se cumplen

**Why:** Check de RC aplicado a acero durante 10+ sesiones.
**How to apply:** LEER el artículo antes de codear. No copiar de otro módulo.
