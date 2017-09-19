#!/bin/bash -ex

UPDATE_FILE=".new-revision-pushed"
IMAGE_NAME="${DOCKER_IMAGE_NAME:-release-notes-json}"

docker build -t "$IMAGE_NAME" --pull .
docker run --rm -v "$PWD:/app" -e RELEASES_URL="http://localhost:8000/rna/all-releases.json" "$IMAGE_NAME"

# UPDATE_FILE is an indicator we can use in Jenkins
# to run other jobs if there was, in fact, an update
rm -f "$UPDATE_FILE"

if [[ "$1" == "commit" ]]; then
    if git status --porcelain | grep -E "\.json$"; then
        git add ./releases/
        git commit -m "Update release data"
        git rev-parse HEAD > "$UPDATE_FILE"
        echo "Release data update committed"
    else
        echo "No new release updates"
    fi
fi
