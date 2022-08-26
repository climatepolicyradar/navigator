#!/bin/bash
set -e

if [ "$#" -ne 2 ]; then
    echo "Pushes a container image to ECR with tags"
    echo 
    echo "Usage: $0 project input_tag"
    echo "Example: $0 container-name 6cd9d7ebad4f16ef7273a7a831d79d5d5caf4164"
    echo "Relies on the following environment variables:"
    echo "- GITHUB_REF, GITHUB_SHA (GH Action default)"
    echo "- DOCKER_USERNAME, DOCKER_PASSWORD"
    exit 1
fi

project="$1"
image_tag="$2"


# login
DOCKER_REGISTRY="${DOCKER_REGISTRY:-}"
echo "${DOCKER_PASSWORD}" | docker login --username "${DOCKER_USERNAME}" --password-stdin "${DOCKER_REGISTRY}"

name="${DOCKER_REGISTRY}cpr/${project}"
input_image="cpr/${project}:${image_tag}"

if [[ "$GITHUB_REF" == "refs/heads"* ]]; then
    # push `branch-sha` tagged image
    branch="${GITHUB_REF/refs\/heads\//}"
    timestamp=$(date --utc +%Y%m%d.%H%M)
    short_sha=${GITHUB_SHA:0:8}
    docker tag "$input_image" "${name}:${branch}-${short_sha}-${timestamp}"
    docker push "${name}:${branch}-${short_sha}-${timestamp}"
    docker tag "$input_image" "${name}:${branch}-${short_sha}"
    docker push "${name}:${branch}-${short_sha}"

    if [[ "$branch" = "main" ]]; then
        # push `latest` tag
        docker tag "$input_image" "${name}:latest"
        docker push "${name}:latest"
    fi

elif [[ "$GITHUB_REF" =~ refs/tags/v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*) ]]; then
    # push `semver` tagged image
    semver="${GITHUB_REF/refs\/tags\/v/}"
    major="$(echo "${semver}" | cut -d'.' -f1)"
    minor="$(echo "${semver}" | cut -d'.' -f2)"
    patch="$(echo "${semver}" | cut -d'.' -f3)"

    docker tag "$input_image" "${name}:${major}.${minor}.${patch}"
    docker tag "$input_image" "${name}:${major}.${minor}"
    docker tag "$input_image" "${name}:${major}"
    docker push "${name}:${major}.${minor}.${patch}"
    docker push "${name}:${major}.${minor}"
    docker push "${name}:${major}"
else
    echo "${GITHUB_REF} is neither a branch head or valid semver tag"
    echo "No image tagging or pushing was performed because of this."
    exit 1
fi
