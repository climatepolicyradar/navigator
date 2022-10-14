#!/bin/sh
export AWS_PROFILE=dev
export DOCKER_REGISTRY=073457443605.dkr.ecr.eu-west-2.amazonaws.com

docker tag backend_base:latest 073457443605.dkr.ecr.eu-west-2.amazonaws.com/navigator-backend-base:latest
aws ecr get-login-password --region eu-west-2 | \
   docker login --username AWS --password-stdin "${DOCKER_REGISTRY}"
   
docker push 073457443605.dkr.ecr.eu-west-2.amazonaws.com/navigator-backend-base:latest
