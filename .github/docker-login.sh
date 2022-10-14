#!/bin/bash
set -e


[ "${AWS_ACCESS_KEY_ID}" == "" ] && (echo "AWS_ACCESS_KEY_ID is not set" ; exit 1)
[ "${AWS_SECRET_ACCESS_KEY}" == "" ] && (echo "AWS_SECRET_ACCESS_KEY is not set" ; exit 1)


# login
DOCKER_REGISTRY="${DOCKER_REGISTRY:-}"

aws ecr get-login-password --region eu-west-2 | \
    docker login --username AWS --password-stdin "${DOCKER_REGISTRY}"
