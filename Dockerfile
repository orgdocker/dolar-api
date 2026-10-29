# ---------- Etapa 1: builder (compila wheels de dependencias) ----------
FROM python:3.10-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---------- Etapa 2: runtime (imagen final liviana) ----------
FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8081 \
    DATA_SOURCE=mock \
    APP_ENV=production

WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels \
 && useradd --create-home --uid 1001 appuser

# --chown: el usuario no-root debe poder leer el código (evita PermissionError)
COPY --chown=appuser:appuser app/ ./app/
USER appuser

EXPOSE 8081
# Cloud Run / Render / App Runner inyectan $PORT; se respeta en tiempo de ejecución
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 60 app:app"]
