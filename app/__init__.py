import os

from flask import Flask, jsonify, send_from_directory

from .service import get_historico


def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False  # tildes legibles en el JSON
    app.json.sort_keys = False

    @app.get("/")
    def index():
        return jsonify(
            servicio="API Histórico Dólar Colombia por Presidencia",
            endpoints=["/api/historico-dolar", "/dashboard", "/health"],
        )

    @app.after_request
    def cors(resp):
        # Permite consumir la API desde dashboards en otro origen
        resp.headers["Access-Control-Allow-Origin"] = os.getenv("CORS_ORIGIN", "*")
        resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        return resp

    @app.get("/dashboard")
    def dashboard():
        return send_from_directory(app.static_folder, "dashboard.html")

    @app.get("/health")
    def health():
        return jsonify(status="ok", env=os.getenv("APP_ENV", "local"))

    @app.get("/api/historico-dolar")
    def historico_dolar():
        periodos, fuente = get_historico()
        return jsonify(
            pais="Colombia",
            moneda="COP por USD (TRM)",
            rango="1994-2026 (32 años)",
            fuente=fuente,
            total_periodos=len(periodos),
            periodos=periodos,
        )

    @app.errorhandler(404)
    def not_found(_):
        return jsonify(error="Recurso no encontrado"), 404

    return app


app = create_app()
