#!/bin/bash
# User data EC2 (Amazon Linux 2023)
# Instala Docker y Git, clona el repositorio, construye la imagen y ejecuta dolar-api en el puerto 8081.
set -eux

REPO_URL="https://github.com/orgdocker/dolar-api.git"
BRANCH="main"
APP_DIR="/opt/dolar-api"

dnf install -y docker git
systemctl enable --now docker

rm -rf "$APP_DIR"
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
cd "$APP_DIR"

docker build -t dolar-api:latest .
docker rm -f dolar-api 2>/dev/null || true
docker run -d --name dolar-api --restart unless-stopped \
  -p 8081:8081 \
  -e APP_ENV=aws-ec2 \
  -e DATA_SOURCE=mock \
  dolar-api:latest
