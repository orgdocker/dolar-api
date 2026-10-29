#!/bin/bash
# Actualiza la instancia con el último commit del repositorio (ejecutar en EC2 vía Session Manager / SSH)
set -eux
cd /opt/dolar-api
sudo git pull --ff-only
sudo docker build -t dolar-api:latest .
sudo docker rm -f dolar-api || true
sudo docker run -d --name dolar-api --restart unless-stopped -p 8081:8081 -e APP_ENV=aws-ec2 dolar-api:latest
