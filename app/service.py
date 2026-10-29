"""Lógica de negocio: arma la respuesta agrupada por mandato.

Fuentes soportadas (variable de entorno DATA_SOURCE):
  - mock      -> valores de referencia de data.py (por defecto, sin red)
  - datos_gov -> TRM oficial (Superfinanciera) publicada en datos.gov.co
"""
import os
from datetime import date
from functools import lru_cache

import requests

from .data import MOCK_TRM, PERIODOS

# Dataset "Tasa de Cambio Representativa del Mercado - Histórico" (Socrata)
DATOS_GOV_URL = os.getenv(
    "TRM_API_URL", "https://www.datos.gov.co/resource/32sa-8pi3.json"
)
TIMEOUT = int(os.getenv("TRM_API_TIMEOUT", "15"))


def _anios(p):
    return f"{p['inicio'][:4]}-{p['fin'][:4]}"


def _from_mock():
    out = []
    for p in PERIODOS:
        v = MOCK_TRM[p["presidente"]]
        out.append(_build(p, v["min"], v["max"]))
    return out


@lru_cache(maxsize=1)
def _from_datos_gov(cache_key: str):
    """Consulta min/max por mandato con agregaciones SoQL (1 request por mandato).
    cache_key = fecha del día, para refrescar el caché diariamente."""
    out = []
    for p in PERIODOS:
        params = {
            "$select": "min(valor) as min_trm, max(valor) as max_trm",
            "$where": (
                f"vigenciadesde >= '{p['inicio']}T00:00:00' "
                f"AND vigenciadesde < '{p['fin']}T00:00:00'"
            ),
        }
        r = requests.get(DATOS_GOV_URL, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        row = r.json()[0]
        out.append(_build(p, float(row["min_trm"]), float(row["max_trm"])))
    return tuple(out)


def _build(p, mn, mx):
    return {
        "presidente": p["presidente"],
        "anios_gestion": _anios(p),
        "inicio": p["inicio"],
        "fin": p["fin"],
        "dolar_min_cop": round(mn, 2),
        "dolar_max_cop": round(mx, 2),
        "variacion_pct": round((mx - mn) / mn * 100, 2),
    }


def get_historico():
    source = os.getenv("DATA_SOURCE", "mock").lower()
    if source == "datos_gov":
        try:
            return list(_from_datos_gov(date.today().isoformat())), "datos.gov.co (TRM oficial SFC)"
        except Exception as exc:  # degradación controlada
            return _from_mock(), f"mock (fallback: {type(exc).__name__})"
    return _from_mock(), "mock (valores de referencia aproximados)"
