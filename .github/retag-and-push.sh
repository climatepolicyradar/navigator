#!/bin/bash
set -e

script_folder=$(dirname "${BASH_SOURCE[0]}")
source $script_folder/funcs.sh

if [ "$#" -ne 2 ]; then
    echo "Pushes a container image to ECR with tags"
    echo
    echo "Usage: $0 project input_tag"
    echo "Example: $0 container-name 6cd9d7ebad4f16ef7273a7a831d79d5d5caf4164"
    echo "Relies on the following environment variables:"
    echo "- GITHUB_HEAD_REF, GITHUB_REF, GITHUB_SHA (GH Action default)"
    echo "- AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, DOCKER_REGISTRY"
    exit 1
fi

[ "${AWS_ACCESS_KEY_ID}" == "" ] && (echo "AWS_ACCESS_KEY_ID is not set" ; exit 1)
[ "${AWS_SECRET_ACCESS_KEY}" == "" ] && (echo "AWS_SECRET_ACCESS_KEY is not set" ; exit 1)
[ "${DOCKER_REGISTRY}" == "" ] && (echo "DOCKER_REGISTRY is not set" ; exit 1)

project="$1"
image_tag="$2"

# login
# This should now be performed as a GA
# See: https://docs.docker.com/build/ci/github-actions/#step-three-define-the-workflow-steps

name=$(clean_string "${DOCKER_REGISTRY}/${project}")
input_image="${project}:${image_tag}"

echo "-------------"
echo "Input       : ${project}:${image_tag}"
echo "Output      : ${name}"
echo "GitRef      : ${GITHUB_REF}"
echo "GitHeadRef  : ${GITHUB_HEAD_REF}"
echo "Branch      : ${GITHUB_REF/refs\/heads\//}"
echo "Repo Tag    : ${name}"
echo "-------------"

docker_tag() {
    echo "Re-tagging $1 -> $2"
    docker tag $1 $2
}

timestamp=$(date --utc -Iseconds | cut -c1-19 | tr -c '[0-9]T\n' '-')
short_sha=${GITHUB_SHA:0:8}

if [[ "${GITHUB_REF}" == "refs/heads"* ]]; then
    # push `branch-sha` tagged image

    # NOTE: Looks like the behaviour has changed for GITHHUB_REF
    # See: https://github.com/semantic-release/env-ci/issues/157
    # ... branches will no longer be handled here but in the 'else' statement below.

    branch="${GITHUB_REF/refs\/heads\//}"
    echo "Detected Branch: ${branch}"


    # Only update latest if on main
    if [[ "${branch}" = "main" ]]; then
        # push `latest` tag
        docker_tag "${input_image}" "${name}:latest"
        docker push "${name}:latest"
        # Also tag for any versioning that might get done
        docker_tag "${input_image}" "${name}:${branch}-${timestamp}-${short_sha}"
        docker push "${name}:${branch}-${timestamp}-${short_sha}"
        # Also tag for any versioning that might get done
        docker_tag "${input_image}" "${name}:${branch}-${short_sha}"
        docker push "${name}:${branch}-${short_sha}"
    fi
elif is_tagged_version ${GITHUB_REF} ; then
    # push `semver` tagged image
    semver="${GITHUB_REF/refs\/tags\/v/}"
    echo "Detected Tag: ${semver}"
    major=$(get_major "${semver}")
    minor=$(get_minor "${semver}")
    patch=$(get_patch "${semver}")
    maturity=$(get_maturity "${semver}")
    echo "Detected Version: ${major} . ${minor} . ${patch} [${maturity}]"

    docker_tag "${input_image}" "${name}:${major}.${minor}.${patch}-${maturity}"
    docker_tag "${input_image}" "${name}:${major}.${minor}-${maturity}"
    docker_tag "${input_image}" "${name}:${major}-${maturity}"
    docker push "${name}:${major}.${minor}.${patch}-${maturity}"
    docker push "${name}:${major}.${minor}-${maturity}"
    docker push "${name}:${major}-${maturity}"
else
    echo "${GITHUB_REF} is neither a branch head nor valid semver tag"
    echo "Assuming '${GITHUB_HEAD_REF}' is a branch"
    if [[ -n "${GITHUB_HEAD_REF}" ]]; then
        branch="$(echo ${GITHUB_HEAD_REF}| tr -c '[0-9,A-Z,a-z]' '-')"
        docker_tag "${input_image}" "${name}:${branch}-${timestamp}-${short_sha}"
        docker push "${name}:${branch}-${timestamp}-${short_sha}"
    else
        echo "No branch found, not a PR so not publishing."
    fi
fi
