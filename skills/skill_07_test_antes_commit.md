---
name: test-antes-de-commit
description: Antes de cada commit — verificar syntax, import, y al menos 1 caso de ejecución real. No commitear código que no compila.
type: feedback
originSessionId: a0d34ba2-2a13-421f-b624-f0f12c1a7219
---
# Test Antes de Commit

## Aplica a: CUALQUIER proyecto de software

## Protocolo pre-commit
```bash
# 1. Syntax check de cada archivo modificado
python -c "import ast; ast.parse(open('file.py').read())"

# 2. Import check
python -c "from module import function"

# 3. Smoke test (al menos 1 ejecución real)
python -c "from motor import disenar; disenar(inputs_minimos)"

# 4. Si hay endpoint: curl real
curl -s http://localhost:8000/endpoint
```

## Anti-patrón: el "Commit y Veremos"
```
MAL: git commit → deploy → 500 Internal Server Error
BIEN: syntax OK → import OK → smoke test OK → commit → deploy → curl OK
```

## Checklist
- [ ] `ast.parse()` de cada .py modificado
- [ ] Import de cada módulo modificado
- [ ] Al menos 1 caso real ejecutado sin error
- [ ] Si hay endpoints: probados con curl
- [ ] Si hay frontend: `npm run build` sin errores

**Why:** Commits con UnboundLocalError, kwargs not defined, syntax errors en producción.
**How to apply:** SIEMPRE antes de `git commit`. Sin excepciones.
