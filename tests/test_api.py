from app import create_app


def client():
    return create_app().test_client()


def test_health():
    r = client().get("/health")
    assert r.status_code == 200 and r.get_json()["status"] == "ok"


def test_historico_dolar(monkeypatch):
    monkeypatch.setenv("DATA_SOURCE", "mock")
    body = client().get("/api/historico-dolar").get_json()
    assert body["total_periodos"] == 8
    for p in body["periodos"]:
        assert {"presidente", "anios_gestion", "dolar_min_cop", "dolar_max_cop"} <= p.keys()
        assert p["dolar_min_cop"] <= p["dolar_max_cop"]
    assert body["periodos"][0]["anios_gestion"] == "1994-1998"
    assert body["periodos"][-1]["anios_gestion"] == "2022-2026"


def test_fallback_si_falla_fuente_externa(monkeypatch):
    monkeypatch.setenv("DATA_SOURCE", "datos_gov")
    monkeypatch.setenv("TRM_API_TIMEOUT", "1")
    import app.service as s
    s.DATOS_GOV_URL = "http://127.0.0.1:9/no-existe"
    s._from_datos_gov.cache_clear()
    body = client().get("/api/historico-dolar").get_json()
    assert body["fuente"].startswith("mock (fallback")


def test_dashboard_y_cors():
    c = client()
    r = c.get("/dashboard")
    assert r.status_code == 200 and b"historico-dolar" in r.data
    assert c.get("/api/historico-dolar").headers["Access-Control-Allow-Origin"] == "*"
