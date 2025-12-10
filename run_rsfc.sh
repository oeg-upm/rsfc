#!/bin/bash
set -e

REPO_URL=""
TEST_ID=""
FTR_FLAG=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --repo)
            REPO_URL="$2"
            shift 2
            ;;
        --id)
            TEST_ID="$2"
            shift 2
            ;;
        --ftr)
            FTR_FLAG=true
            shift
            ;;
        *)
            echo "Unknown argument: $1"
            echo "Usage: $0 --repo <repo_url> [--ftr] [--id <test_id>]"
            exit 1
            ;;
    esac
done


if [ -z "$REPO_URL" ]; then
    echo "Error: --repo is required"
    exit 1
fi

OUTPUT_DIR="rsfc_output"
mkdir -p "$OUTPUT_DIR"


DOCKER_ARGS="--repo $REPO_URL"
if [ "$FTR_FLAG" = true ]; then
    DOCKER_ARGS="$DOCKER_ARGS --ftr"
fi
if [ -n "$TEST_ID" ]; then
    DOCKER_ARGS="$DOCKER_ARGS --id $TEST_ID"
fi


docker run --rm -v "$(pwd)/$OUTPUT_DIR:/rsfc/rsfc_output" -e PYTHONWARNINGS="ignore" rsfc-docker $DOCKER_ARGS
