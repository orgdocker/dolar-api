# API Histórico del Dólar en Colombia por Presidencia

Web Service REST (Python + Flask) que expone el precio **mínimo y máximo de la TRM (COP/USD)** por cada período presidencial de Colombia entre **ago-1994 y ago-2026 (32 años, 8 mandatos)**. Se empaqueta con Docker y se despliega en **Google Cloud Run**.

## 1. Estructura

```
dolar-presidencial-api/
├── app/
│   ├── __init__.py      # Flask app factory + endpoints
│   ├── service.py       # Lógica: mock o TRM oficial (datos.gov.co)
│   └── data.py          # Períodos presidenciales + mock data
├── tests/test_api.py    # Pruebas con pytest
├── requirements.txt
├── Dockerfile           # Multi-etapa, python:3.10-slim, usuario no-root
├── .dockerignore
└── .gitignore
```

## 2. Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Información del servicio |
| GET | `/health` | Health check |
| GET | `/api/historico-dolar` | Mín./máx. del dólar por mandato |

## 3. Variables de entorno

| Variable | Default | Uso |
|---|---|---|
| `PORT` | `8081` | Puerto de escucha (la nube lo inyecta) |
| `DATA_SOURCE` | `mock` | `mock` o `datos_gov` (TRM oficial SFC vía datos.gov.co) |
| `TRM_API_URL` | dataset `32sa-8pi3` | URL Socrata de la TRM |
| `TRM_API_TIMEOUT` | `15` | Timeout (s) de la consulta externa |
| `APP_ENV` | `production` | Etiqueta del entorno |

> Los valores `mock` son **aproximados** y solo de ejemplo. Con `DATA_SOURCE=datos_gov` el servicio calcula min/max exactos sobre la serie oficial; si la fuente falla, responde con mock e indica el fallback en el campo `fuente`.

## 4. Ejecución local (sin Docker)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt pytest
pytest -q
flask --app app run --port 8081
curl http://localhost:8081/api/historico-dolar
```

## 5. Docker

```bash
docker build -t dolar-api:1.0 .
docker run --rm -p 8081:8081 --name dolar-api dolar-api:1.0
# Con datos oficiales:
docker run --rm -p 8081:8081 -e DATA_SOURCE=datos_gov dolar-api:1.0
curl http://localhost:8081/api/historico-dolar
```

## 6. Despliegue en Google Cloud Run

```bash
export PROJECT_ID=mi-proyecto-gcp
export REGION=us-central1
export SERVICE=dolar-api

gcloud auth login
gcloud config set project $PROJECT_ID
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

gcloud artifacts repositories create apis --repository-format=docker --location=$REGION
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/apis/$SERVICE:1.0

gcloud run deploy $SERVICE \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/apis/$SERVICE:1.0 \
  --region $REGION --platform managed \
  --allow-unauthenticated \
  --port 8081 \
  --set-env-vars DATA_SOURCE=datos_gov,APP_ENV=production \
  --memory 256Mi --cpu 1 --min-instances 0 --max-instances 3

URL=$(gcloud run services describe $SERVICE --region $REGION --format 'value(status.url)')
curl $URL/api/historico-dolar
```

Actualizar variables sin redesplegar imagen:

```bash
gcloud run services update $SERVICE --region $REGION --update-env-vars DATA_SOURCE=mock
```

## 7. Entregables

1. **Repositorio de código** (GitHub/GitLab, público o con acceso al docente) con: código fuente, `requirements.txt`, `Dockerfile`, pruebas y este README.
2. **Demostración en vivo**: URL pública activa (ej. `https://dolar-api-xxxx.a.run.app/api/historico-dolar`). En su defecto, capturas de Postman/curl contra producción que muestren: status `200`, el JSON con los 8 mandatos y el `/health` respondiendo.

## 8. Dashboard

Dashboard en HTML + Tailwind + JavaScript (Chart.js) en `app/static/dashboard.html`.

- Servido por la propia API: `http://<IP-PUBLICA>:8081/dashboard` (mismo origen, sin problemas de CORS).
- Abierto como archivo local: consume `http://52.3.230.46:8081/api/historico-dolar` (la API envía `Access-Control-Allow-Origin`; se puede restringir con la variable `CORS_ORIGIN`).

## 9. Despliegue en AWS EC2 (capa gratuita)

Repositorio: https://github.com/orgdocker/dolar-api

1. EC2 → Lanzar instancia: Amazon Linux 2023, `t3.micro`, sin par de claves.
2. Grupo de seguridad: regla de entrada TCP **8081** desde `0.0.0.0/0`.
3. Detalles avanzados → Datos de usuario: pegar `deploy/ec2-user-data.sh` (clona el repo, construye y ejecuta el contenedor).
4. Esperar 3–5 min y abrir `http://<IP-PUBLICA>:8081/dashboard`.

Para actualizar tras un nuevo push: ejecutar `deploy/redeploy.sh` en la instancia, o relanzarla.
