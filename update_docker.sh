#!/bin/bash

set -exo pipefail

UPDATE_FILE=".new-revision-pushed"
IMAGE_NAME="${DOCKER_IMAGE_NAME:-release-notes-json}"
IMAGE_NAME="${IMAGE_NAME}:$(git rev-parse HEAD)"

function imageExists() {
    docker history -q "${IMAGE_NAME}" > /dev/null 2>&1
    return $?
}

if ! imageExists; then
    docker build -t "$IMAGE_NAME" --pull .
fi

docker run -u $(id -u) --rm -v "$PWD:/app" "$IMAGE_NAME"

if [[ "$1" == "commit" ]]; then
    if git status --porcelain | grep -E "\.json$"; then
        git add ./releases/
        git commit -m "Update release data"
        git push git@github.com:mozilla/release-notes.git HEAD:master
        echo "Release data update committed"
    else
        echo "No new release updates"
    fi
fi

if [[ -n "$SNITCH_URL" ]]; then
    curl "$SNITCH_URL"
fi
