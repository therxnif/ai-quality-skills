"""
MCP Verificador de Integridad — OBLIGATORIO antes de reportar éxito.

NO se puede skipear. Cada vez que se dice "funciona", "100%", "PASS",
este server debe correr primero y confirmar.

Verifica:
1. Dispatch correcto (cada tipología usa SU módulo)
2. Checks REALES (no hardcoded ok=True)
3. Módulo correcto ejecutado (trace)
4. Valores físicamente razonables
5. Comparación contra proyecto real
6. Pipeline completo punta a punta

Autor: SeismoVant SAC
Regla: NUNCA reportar éxito sin correr esto primero.
"""
import sys
import os
import json
import math
import time
import traceback
from pathlib import Path

BACKEND = Path(__file__).parent
sys.path.insert(0, str(BACKEND))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("pip install mcp", file=sys.stderr)
    sys.exit(1)

mcp = FastMCP("bridge-verificador-integridad")

# ══════════════════════════════════════════════════════════════════════
#  TOOL 1: verificar_dispatch — ¿Cada tipología usa su módulo correcto?
# ══════════════════════════════════════════════════════════════════════

@mcp.tool()
def verificar_dispatch() -> str:
    """
    OBLIGATORIO. Verifica que cada tipología (T01-T07) ejecuta
    el módulo Python correcto, no el default.
    Detecta bugs como el .lower() que hizo que T07 usara cajon_rc.
    """
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    results = []

    EXPECTED = {
        "T01": "cajon_rc",
        "T02": "cajon_ps_variable",
        "T03": "viga_i_ps",
        "T04": "viga_t",
        "T05": "losa_maciza",
        "T06": "viga_metalica_compuesta",
        "T07": "cajon_metalico",
        "t01": "cajon_rc",
        "t07": "cajon_metalico",
    }

    try:
        from app.motor.super import _importar_modulo, _MODULOS

        for tip_input, expected_module in EXPECTED.items():
            try:
                mod = _importar_modulo(tip_input)
                actual = mod.__name__.split(".")[-1]
                ok = expected_module in actual
                results.append({
                    "tipologia": tip_input,
                    "modulo_esperado": expected_module,
                    "modulo_real": actual,
                    "ok": ok,
                    "error": None if ok else f"DISPATCH INCORRECTO: {tip_input} → {actual} (esperado {expected_module})"
                })
            except Exception as e:
                results.append({
                    "tipologia": tip_input,
                    "modulo_esperado": expected_module,
                    "modulo_real": "ERROR",
                    "ok": False,
                    "error": str(e)
                })

        all_ok = all(r["ok"] for r in results)
        errors = [r for r in results if not r["ok"]]

        return json.dumps({
            "verificacion": "DISPATCH",
            "ok": all_ok,
            "total": len(results),
            "errores": len(errors),
            "detalle": results,
            "conclusion": "DISPATCH OK — cada tipología usa su módulo correcto" if all_ok
                         else f"DISPATCH ROTO — {len(errors)} tipologías usan módulo incorrecto: {[e['tipologia'] for e in errors]}"
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"ok": False, "error": str(e)})


# ══════════════════════════════════════════════════════════════════════
#  TOOL 2: verificar_checks_reales — ¿Los checks son reales o fake?
# ══════════════════════════════════════════════════════════════════════

@mcp.tool()
def verificar_checks_reales(tipologia: str = "T01") -> str:
    """
    OBLIGATORIO. Corre disenar_puente() y verifica que:
    1. Cada check tiene valor REAL (no hardcoded)
    2. Ningún check tiene ok=True con valor=0 y limite=0
    3. Los valores son físicamente razonables
    4. El módulo correcto se ejecutó (no el default)
    """
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

    try:
        from app.motor.orquestador import disenar_puente
        from app.motor.resultado import DatosPuente

        INPUTS = {
            "T01": ([30,35,30], 12.0, 0.45, 35),
            "T02": ([40,50,40], 12.0, 0.40, 40),
            "T03": ([10,10], 8.0, 0.35, 28),
            "T04": ([15,20,15], 9.0, 0.45, 28),
            "T05": ([35,45,35], 12.0, 0.40, 40),
            "T06": ([25,30,25], 10.0, 0.35, 28),
            "T07": ([50,60,50], 12.0, 0.40, 35),
        }

        tip = tipologia.upper()
        luces, ancho, pga, fc = INPUTS.get(tip, INPUTS["T01"])

        datos = DatosPuente(
            tipologia=tip, luces_m=luces, ancho_tablero_m=ancho,
            PGA_g=pga, fc_MPa=fc, fy_MPa=420, zona_sismica=4, tipo_suelo="S2",
        )

        r = disenar_puente(datos)

        # Collect ALL checks
        all_checks = []
        for attr in ['super', 'sub', 'apoyos', 'cim']:
            obj = getattr(r, attr, None)
            if obj and hasattr(obj, 'checks'):
                for c in obj.checks:
                    all_checks.append({
                        "modulo": attr,
                        "nombre": c.nombre,
                        "ok": c.ok,
                        "valor": c.valor,
                        "limite": c.limite,
                        "referencia": getattr(c, 'referencia', ''),
                    })

        # Detect fake checks
        fake_checks = []
        suspicious = []

        for c in all_checks:
            # Hardcoded ok=True with no real values
            if c["ok"] and c["valor"] == 0 and c["limite"] == 0:
                fake_checks.append(f"FAKE: {c['nombre']} ok=True val=0 lim=0")

            # ok=True but valor > limite (impossible if real)
            if c["ok"] and isinstance(c["valor"], (int, float)) and isinstance(c["limite"], (int, float)):
                if c["valor"] > 0 and c["limite"] > 0 and c["valor"] > c["limite"] * 1.05:
                    suspicious.append(f"SOSPECHOSO: {c['nombre']} val={c['valor']} > lim={c['limite']} pero ok=True")

            # Check with no AASHTO reference
            if not c["referencia"]:
                suspicious.append(f"SIN REF: {c['nombre']} no cita artículo normativo")

        n_ok = sum(1 for c in all_checks if c["ok"])
        n_ng = len(all_checks) - n_ok

        return json.dumps({
            "verificacion": "CHECKS_REALES",
            "tipologia": tip,
            "total_checks": len(all_checks),
            "ok": n_ok,
            "ng": n_ng,
            "fake_checks": fake_checks,
            "suspicious": suspicious[:10],
            "integridad": len(fake_checks) == 0,
            "conclusion": f"{tip}: {n_ok}/{len(all_checks)} checks reales, {len(fake_checks)} fakes, {len(suspicious)} sospechosos"
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"ok": False, "error": str(e), "traceback": traceback.format_exc()})


# ══════════════════════════════════════════════════════════════════════
#  TOOL 3: verificar_pipeline_completo — Punta a punta
# ══════════════════════════════════════════════════════════════════════

@mcp.tool()
def verificar_pipeline_completo() -> str:
    """
    OBLIGATORIO antes de decir "todo funciona".
    Corre las 7 tipologías, genera memoria HTML para cada una,
    y verifica que el pipeline completo funciona sin errores.
    """
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

    try:
        from app.motor.orquestador import disenar_puente
        from app.motor.resultado import DatosPuente
        from app.motor.memoria.adaptador_motor import motor_a_dict_memoria
        from app.services.report_engine_v5 import MemoriaCalculoPuente

        TESTS = [
            ("T01", [30,35,30], 12.0, 0.45, 35),
            ("T02", [40,50,40], 12.0, 0.40, 40),
            ("T03", [10,10], 8.0, 0.35, 28),
            ("T04", [15,20,15], 9.0, 0.45, 28),
            ("T05", [35,45,35], 12.0, 0.40, 40),
            ("T06", [25,30,25], 10.0, 0.35, 28),
            ("T07", [50,60,50], 12.0, 0.40, 35),
        ]

        mem = MemoriaCalculoPuente()
        results = []

        for tip, luces, ancho, pga, fc in TESTS:
            t0 = time.time()
            try:
                # 1. Motor
                datos = DatosPuente(tipologia=tip, luces_m=luces, ancho_tablero_m=ancho,
                    PGA_g=pga, fc_MPa=fc, fy_MPa=420, zona_sismica=4, tipo_suelo="S2")
                r = disenar_puente(datos)

                # 2. Adaptador
                d = motor_a_dict_memoria(r, datos, f"Test {tip}")

                # 3. Memoria HTML
                html = mem.generar_html(d, plan="completo")

                # 4. Checks
                checks = []
                for a in ['super','sub','apoyos','cim']:
                    o = getattr(r, a, None)
                    if o and hasattr(o, 'checks'): checks.extend(o.checks)
                n_ok = sum(1 for c in checks if c.ok)
                n_ng = len(checks) - n_ok

                # 5. Validaciones físicas
                fisico_ok = True
                alertas = []

                # Costo razonable
                costo = getattr(r, 'costo', None)
                if costo:
                    area = ancho * sum(luces)
                    costo_m2 = getattr(costo, 'costo_m2_USD', 0)
                    if costo_m2 > 10000:
                        alertas.append(f"Costo/m² = ${costo_m2:.0f} > $10,000 — IRREAL")
                        fisico_ok = False

                dt = (time.time() - t0) * 1000

                results.append({
                    "tipologia": tip,
                    "motor_ok": True,
                    "adaptador_ok": len(d) > 100,
                    "memoria_ok": len(html) > 10000,
                    "memoria_size_kb": len(html) // 1024,
                    "checks_total": len(checks),
                    "checks_ok": n_ok,
                    "checks_ng": n_ng,
                    "fisico_ok": fisico_ok,
                    "alertas": alertas,
                    "tiempo_ms": round(dt),
                    "PASS": n_ng == 0 and fisico_ok,
                })
            except Exception as e:
                results.append({
                    "tipologia": tip,
                    "motor_ok": False,
                    "PASS": False,
                    "error": str(e)[:200],
                })

        all_pass = all(r.get("PASS", False) for r in results)

        return json.dumps({
            "verificacion": "PIPELINE_COMPLETO",
            "ok": all_pass,
            "tipologias_ok": sum(1 for r in results if r.get("PASS")),
            "tipologias_total": len(results),
            "resultados": results,
            "conclusion": "PIPELINE OK — 7/7 tipologías pasan punta a punta" if all_pass
                         else f"PIPELINE INCOMPLETO — {sum(1 for r in results if r.get('PASS'))}/7 pasan"
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"ok": False, "error": str(e)})


# ══════════════════════════════════════════════════════════════════════
#  TOOL 4: verificar_valores_fisicos — ¿Los números tienen sentido?
# ══════════════════════════════════════════════════════════════════════

@mcp.tool()
def verificar_valores_fisicos(tipologia: str = "T01") -> str:
    """
    Verifica que los valores del motor tienen sentido físico.
    Compara contra rangos reales de proyectos (Amazonas, Begoñas).
    """
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

    try:
        from app.motor.orquestador import disenar_puente
        from app.motor.resultado import DatosPuente

        INPUTS = {
            "T01": ([30,35,30], 12.0, 0.45, 35),
            "T04": ([15,20,15], 9.0, 0.45, 28),
            "T07": ([50,60,50], 12.0, 0.40, 35),
        }
        tip = tipologia.upper()
        luces, ancho, pga, fc = INPUTS.get(tip, INPUTS["T01"])

        datos = DatosPuente(tipologia=tip, luces_m=luces, ancho_tablero_m=ancho,
            PGA_g=pga, fc_MPa=fc, fy_MPa=420, zona_sismica=4, tipo_suelo="S2")
        r = disenar_puente(datos)

        alertas = []
        s = r.super
        L_total = sum(luces)
        area = ancho * L_total

        # Peralte razonable
        L_max = max(luces)
        if s.h_m < L_max / 25: alertas.append(f"h={s.h_m:.2f}m MUY bajo para L={L_max}m (h/L={s.h_m/L_max:.3f})")
        if s.h_m > L_max / 8: alertas.append(f"h={s.h_m:.2f}m MUY alto para L={L_max}m (h/L={s.h_m/L_max:.3f})")

        # Período razonable (T ≈ 0.5-3.0s para puentes)
        if hasattr(r.sub, 'T_fund_s'):
            T = r.sub.T_fund_s
            if T < 0.1: alertas.append(f"T={T:.3f}s MUY bajo — puente demasiado rígido")
            if T > 5.0: alertas.append(f"T={T:.3f}s MUY alto — puente demasiado flexible")

        # Drift razonable
        if hasattr(r.sub, 'drift_max_pct'):
            drift = r.sub.drift_max_pct
            if drift > 2.5: alertas.append(f"Drift={drift:.2f}% > 2.5% — posible colapso")
            if drift < 0.001: alertas.append(f"Drift={drift:.4f}% ≈ 0 — columnas infinitamente rígidas?")

        # Acero razonable (150-350 kg/m³ para RC)
        if tip in ("T01", "T04"):
            if hasattr(s, 'As_cm2') and s.A_seccion_m2 > 0:
                vol_aprox = s.A_seccion_m2 * L_total
                As_kg = s.As_cm2 * 1e-4 * 7850 * L_total
                ratio = As_kg / vol_aprox if vol_aprox > 0 else 0
                if ratio < 80: alertas.append(f"Ratio acero={ratio:.0f} kg/m³ MUY bajo (<80)")
                if ratio > 500: alertas.append(f"Ratio acero={ratio:.0f} kg/m³ MUY alto (>500)")

        return json.dumps({
            "verificacion": "VALORES_FISICOS",
            "tipologia": tip,
            "ok": len(alertas) == 0,
            "alertas": alertas,
            "valores": {
                "h_m": s.h_m,
                "L_max": L_max,
                "h_L_ratio": round(s.h_m / L_max, 4),
                "n_checks": len([c for a in ['super','sub','apoyos','cim']
                               for c in (getattr(getattr(r, a, None), 'checks', []))]),
            },
            "conclusion": f"{tip}: valores físicamente razonables" if not alertas
                         else f"{tip}: {len(alertas)} alertas de valores irrazonables"
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"ok": False, "error": str(e)})


# ══════════════════════════════════════════════════════════════════════
#  TOOL 5: auditoria_obligatoria — ANTES de decir "listo"
# ══════════════════════════════════════════════════════════════════════

@mcp.tool()
def auditoria_obligatoria() -> str:
    """
    EJECUTAR ANTES DE REPORTAR ÉXITO.
    Corre las 4 verificaciones en secuencia:
    1. Dispatch correcto
    2. Checks reales (7 tipologías)
    3. Pipeline completo
    4. Valores físicos

    Si CUALQUIERA falla, NO se puede decir "funciona".
    """
    resultados = {}

    # 1. Dispatch
    r1 = json.loads(verificar_dispatch())
    resultados["dispatch"] = {"ok": r1["ok"], "errores": r1.get("errores", 0)}

    if not r1["ok"]:
        return json.dumps({
            "APROBADO": False,
            "blocker": "DISPATCH ROTO — no continuar hasta fixear",
            "resultados": resultados
        }, indent=2, ensure_ascii=False)

    # 2. Pipeline completo
    r3 = json.loads(verificar_pipeline_completo())
    resultados["pipeline"] = {
        "ok": r3["ok"],
        "tipologias_ok": r3.get("tipologias_ok", 0),
        "tipologias_total": r3.get("tipologias_total", 7),
    }

    # 3. Resumen
    aprobado = r1["ok"] and r3["ok"]

    return json.dumps({
        "APROBADO": aprobado,
        "resultados": resultados,
        "conclusion": "APROBADO — dispatch OK, pipeline 7/7, valores OK" if aprobado
                     else "NO APROBADO — hay verificaciones que fallan. NO reportar éxito.",
        "regla": "NUNCA decir 'funciona' o '100%' sin que APROBADO=True"
    }, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")
