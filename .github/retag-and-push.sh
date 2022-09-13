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

[ "${AWS_ACCESS_KEY_ID}" == "" ] && (echo "AWS_ACCESS_KEY_ID is not set" ; exit 1)
[ "${AWS_SECRET_ACCESS_KEY}" == "" ] && (echo "AWS_SECRET_ACCESS_KEY is not set" ; exit 1)

project="$1"
image_tag="$2"

# login
DOCKER_REGISTRY="${DOCKER_REGISTRY:-}"

aws ecr get-login-password --region eu-west-2 | \
    docker login --username AWS --password-stdin "${DOCKER_REGISTRY}"

name="$(echo "${DOCKER_REGISTRY}/${project}" | tr -d '\n' | tr -d ' ')"
input_image="${project}:${image_tag}"

echo "Input:   ${project}:${image_tag}"
echo "Output:  ${name}"
echo "GitRef:  ${GITHUB_REF}"
echo "Branch:  ${GITHUB_REF/refs\/heads\//}"
echo "Repo Tag ${name}"

timestamp=$(date --utc +%Y%m%d.%H%M.%S%N)
short_sha=${GITHUB_SHA:0:8}

if [[ "${GITHUB_REF}" == "refs/heads"* ]]; then
    # push `branch-sha` tagged image
    branch="${GITHUB_REF/refs\/heads\//}"
    if [[ "${branch}" = "main" ]]; then
        # push a `version` tag
        docker tag "${input_image}" "${name}:${branch}-${timestamp}_${short_sha}"
        docker push "${name}:${branch}-${timestamp}_${short_sha}"
        # push `latest` tag
        docker tag "${input_image}" "${name}:latest"
        docker push "${name}:latest"
    fi
elif [[ "${GITHUB_REF}" =~ refs/tags/v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*) ]]; then
    # push `semver` tagged image
    semver="${GITHUB_REF/refs\/tags\/v/}"
    major="$(echo "${semver}" | cut -d'.' -f1)"
    minor="$(echo "${semver}" | cut -d'.' -f2)"
    patch="$(echo "${semver}" | cut -d'.' -f3)"

    docker tag "${input_image}" "${name}:${major}.${minor}.${patch}"
    docker tag "${input_image}" "${name}:${major}.${minor}"
    docker tag "${input_image}" "${name}:${major}"
    docker push "${name}:${major}.${minor}.${patch}"
    docker push "${name}:${major}.${minor}"
    docker push "${name}:${major}"
else
    echo "${GITHUB_REF} is neither a branch head or valid semver tag"
    if [[ -n "${GITHUB_HEAD_REF}" ]]; then
        branch="${GITHUB_HEAD_REF}"
        echo "Not yet publishing for branches, so not publishing for '${branch}'."
        # docker images
        # docker tag "${input_image}" "${name}:${branch}-${timestamp}-${short_sha}"
        # docker images
        # docker push "${name}:${branch}-${short_sha}-${timestamp}"
    else
        echo "No branch found, not a PR so not publishing."
    fi
fi