#!/bin/bash
set -e

REPO_URL=""
LOCAL_PATH=""
METADATA_PATH=""
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
        --local)
            LOCAL_PATH="$2"
            shift 2
            ;;
        --metadata)
            METADATA_PATH="$2"
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
            echo "Usage: $0 (--repo <repo_url> | --local <local_path>) [--metadata <metadata_file>] [--ftr] [--id <test_id>] [-t <github_token>] [-b <branch>] [-v <tag>]"
            exit 1
            ;;
    esac
done

if [ -n "$REPO_URL" ] && [ -n "$LOCAL_PATH" ]; then
    echo "Error: You cannot use '--repo' and '--local' at the same time."
    exit 1
fi

if [ -z "$REPO_URL" ] && [ -z "$LOCAL_PATH" ]; then
    echo "Error: Either '--repo' or '--local' must be provided."
    exit 1
fi

if [ -n "$LOCAL_PATH" ] && { [ -n "$BRANCH" ] || [ -n "$TAG" ] || [ -n "$TOKEN" ]; }; then
    echo "Error: Remote options (-b, -v, -t) cannot be used with '--local'."
    exit 1
fi

OUTPUT_DIR="rsfc_output"
mkdir -p "$OUTPUT_DIR"

VOLUME_MOUNTS=""
DOCKER_ARGS=""

if [ -n "$REPO_URL" ]; then
    DOCKER_ARGS="--repo $REPO_URL"
elif [ -n "$LOCAL_PATH" ]; then
    ABS_LOCAL_PATH=$(cd "$LOCAL_PATH" && pwd)
    VOLUME_MOUNTS="-v $ABS_LOCAL_PATH:/rsfc/target_repo"
    DOCKER_ARGS="--local /rsfc/target_repo"
fi

if [ -n "$METADATA_PATH" ]; then
    ABS_METADATA_PATH=$(cd "$(dirname "$METADATA_PATH")" && pwd)/$(basename "$METADATA_PATH")
    VOLUME_MOUNTS="$VOLUME_MOUNTS -v $ABS_METADATA_PATH:/rsfc/somef_metadata.json"
    DOCKER_ARGS="$DOCKER_ARGS --metadata /rsfc/somef_metadata.json"
fi

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
    $VOLUME_MOUNTS \
    -e PYTHONWARNINGS="ignore" \
    rsfc-docker \
    $DOCKER_ARGS