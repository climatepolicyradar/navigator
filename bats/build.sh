#!/bin/bash

cd $(git rev-parse --show-toplevel)/bats

[ -d "temp_clone_dir" ] && rm -rf "temp_clone_dir"
mkdir temp_clone_dir 
git clone https://github.com/ztombol/bats-support temp_clone_dir/bats-support
git clone https://github.com/ztombol/bats-assert temp_clone_dir/bats-assert
git clone https://github.com/lox/bats-mock temp_clone_dir/lox-bats-mock

cd $(git rev-parse --show-toplevel)
docker build bats -t bats-with-helpers:latest
