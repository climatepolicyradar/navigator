#!/usr/bin/env bats

@test "func1 function should return 1" {
  source /code/example1.sh
  run func1
  [ "$status" -eq 1 ]
}

@test "func1 function should return 2" {
  source /code/example1.sh
  run func1
  [ "$status" -eq 2]
}