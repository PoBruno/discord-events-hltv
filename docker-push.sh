#!/bin/bash

# Nome da imagem no Docker Hub
IMAGE_NAME="lorthe/discord-hltv-matches"
TAG="latest"

# Docker compose build
docker compose build

# Realizar o push para o Docker Hub
docker push $IMAGE_NAME:$TAG

echo "Imagem '$IMAGE_NAME:$TAG' foi enviada para o Docker Hub."
