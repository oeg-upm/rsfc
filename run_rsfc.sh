#!/bin/bash

# --- Comprobación del parámetro obligatorio ---
if [ -z "$1" ]; then
    echo "Uso: $0 <repo_url> [args_adicionales]"
    echo "Ejemplo: $0 https://github.com/repo --ftr --test_id test123"
    exit 1
fi

REPO_URL="$1"
shift  # quitamos el primer argumento (repo_url) de $@

# --- Construir la imagen Docker ---
echo "Construyendo imagen Docker rsfc-docker..."
docker build -t rsfc-docker . > /dev/null

# --- Construcción de argumentos para el contenedor ---
# El primer argumento siempre es --repo <repo_url>
DOCKER_ARGS="--repo \"$REPO_URL\""

# Añadimos todos los argumentos adicionales que el usuario pasó
for arg in "$@"; do
    DOCKER_ARGS="$DOCKER_ARGS $arg"
done

# --- Carpeta de salida fija ---
OUTPUT_DIR="rsfc_output"
mkdir -p "$OUTPUT_DIR"
echo "Carpeta de salida: $OUTPUT_DIR"

# --- Ejecutar el contenedor ---
CONTAINER_ID=$(eval docker run -d rsfc-docker $DOCKER_ARGS)
echo "Contenedor lanzado: $CONTAINER_ID"

# --- Esperar a que termine ---
docker wait "$CONTAINER_ID" > /dev/null
echo "Contenedor terminado."

# --- Copiar el archivo desde el contenedor ---
docker cp "$CONTAINER_ID:/rsfc/outputs/rsfc_assessment.json" "$OUTPUT_DIR/rsfc_assessment.json"
echo "Archivo copiado a: $OUTPUT_DIR/rsfc_assessment.json"

# --- Borrar el contenedor ---
docker rm "$CONTAINER_ID" > /dev/null
echo "Contenedor eliminado."
