#!/bin/bash

if [ -z "$1" ]; then
    echo "Uso: $0 <repo_url> [--ftr] [--id TESTID]"
    exit 1
fi

REPO_URL="$1"
shift

FTR_FLAG=false
TEST_ID=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --ftr)
            FTR_FLAG=true
            shift
            ;;
        --id)
            TEST_ID="$2"
            shift 2
            ;;
        *)
            echo "Argumento desconocido: $1"
            exit 1
            ;;
    esac
done

DOCKER_ARGS="--repo \"$REPO_URL\""

if [ "$FTR_FLAG" = true ]; then
    DOCKER_ARGS="$DOCKER_ARGS --ftr"
fi

if [ -n "$TEST_ID" ]; then
    DOCKER_ARGS="$DOCKER_ARGS --id \"$TEST_ID\""
fi

echo "Construyendo imagen Docker rsfc-docker..."
docker build -t rsfc-docker .

OUTPUT_DIR="rsfc_output"
mkdir -p "$OUTPUT_DIR"
echo "Carpeta de salida: $OUTPUT_DIR"

CONTAINER_ID=$(eval docker run -d rsfc-docker $DOCKER_ARGS)

echo "Contenedor lanzado: $CONTAINER_ID"

docker wait "$CONTAINER_ID" > /dev/null
echo "Contenedor terminado."

if docker cp "$CONTAINER_ID:/rsfc/outputs/rsfc_assessment.json" "$OUTPUT_DIR/rsfc_assessment.json" 2>/dev/null; then
    echo "Archivo copiado a: $OUTPUT_DIR/rsfc_assessment.json"
else
    echo "❌ El contenedor no generó rsfc_assessment.json"
fi

docker rm "$CONTAINER_ID" > /dev/null
echo "Contenedor eliminado."
