#!/bin/bash

# Idea taken from: https://github.com/moby/moby/issues/31154#issuecomment-360531460
SRC=$1
DEST=$2

test -z "${SRC}" && (echo "no source volume" ; exit 1)
test -z "${DEST}" && (echo "no destination volume" ; exit 1)

# Create bolume if not existing
docker volume ls | grep ${DEST} || docker volume create --name ${DEST}

# Do the copy
docker run --rm -it -v ${SRC}:/from -v ${DEST}:/to alpine ash -c "cd /from ; cp -av . /to"

docker volume ls