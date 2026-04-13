#!/bin/bash
set -e

REPO_URL=""
TEST_ID=""
FTR_FLAG=false
TOKEN=""
BRANCH=""
TAG=""

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
        -t)
            TOKEN="$2"
            shift 2
            ;;
        -b)
            BRANCH="$2"
            shift 2
            ;;
        -v)
            TAG="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            echo "Usage: $0 --repo <repo_url> [--ftr] [--id <test_id>] [-t <github_token>] [-b <branch>] [-v <tag>]"
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

if [ -n "$BRANCH" ]; then
    DOCKER_ARGS="$DOCKER_ARGS -b $BRANCH"
fi

if [ -n "$TAG" ]; then
    DOCKER_ARGS="$DOCKER_ARGS -v $TAG"
fi

if [ "$FTR_FLAG" = true ]; then
    DOCKER_ARGS="$DOCKER_ARGS --ftr"
fi

if [ -n "$TEST_ID" ]; then
    DOCKER_ARGS="$DOCKER_ARGS --id $TEST_ID"
fi

if [ -n "$TOKEN" ]; then
    DOCKER_ARGS="$DOCKER_ARGS -t $TOKEN"
fi

docker run --rm \
    -v "$(pwd)/$OUTPUT_DIR:/rsfc/rsfc_output" \
    -e PYTHONWARNINGS="ignore" \
    rsfc-docker \
    $DOCKER_ARGS