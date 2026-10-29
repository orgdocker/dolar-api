"""Períodos presidenciales de Colombia (ago-1994 a ago-2026 = 32 años)
y valores de referencia de la TRM (COP por USD) por mandato.

IMPORTANTE: los mínimos y máximos de MOCK son aproximados (redondeados) y
sirven solo como datos de ejemplo. Para cifras exactas use DATA_SOURCE=datos_gov,
que calcula min/max a partir de la serie oficial de la TRM.
"""

PERIODOS = [
    {"presidente": "Ernesto Samper Pizano",        "inicio": "1994-08-07", "fin": "1998-08-07"},
    {"presidente": "Andrés Pastrana Arango",       "inicio": "1998-08-07", "fin": "2002-08-07"},
    {"presidente": "Álvaro Uribe Vélez (1er mandato)", "inicio": "2002-08-07", "fin": "2006-08-07"},
    {"presidente": "Álvaro Uribe Vélez (2do mandato)", "inicio": "2006-08-07", "fin": "2010-08-07"},
    {"presidente": "Juan Manuel Santos (1er mandato)", "inicio": "2010-08-07", "fin": "2014-08-07"},
    {"presidente": "Juan Manuel Santos (2do mandato)", "inicio": "2014-08-07", "fin": "2018-08-07"},
    {"presidente": "Iván Duque Márquez",           "inicio": "2018-08-07", "fin": "2022-08-07"},
    {"presidente": "Gustavo Petro Urrego",         "inicio": "2022-08-07", "fin": "2026-08-07"},
]

# Valores aproximados de referencia (COP/USD). Validar contra la TRM oficial.
MOCK_TRM = {
    "Ernesto Samper Pizano":            {"min": 806.00,  "max": 1397.00},
    "Andrés Pastrana Arango":           {"min": 1375.00, "max": 2683.00},
    "Álvaro Uribe Vélez (1er mandato)": {"min": 2206.00, "max": 2968.88},
    "Álvaro Uribe Vélez (2do mandato)": {"min": 1652.41, "max": 2596.37},
    "Juan Manuel Santos (1er mandato)": {"min": 1748.41, "max": 2054.90},
    "Juan Manuel Santos (2do mandato)": {"min": 1846.12, "max": 3434.89},
    "Iván Duque Márquez":               {"min": 2850.00, "max": 4153.91},
    "Gustavo Petro Urrego":             {"min": 3190.00, "max": 5061.21},
}
