#!/usr/bin/env bats
load '/opt/bats-test-helpers/bats-support/load.bash'
load '/opt/bats-test-helpers/bats-assert/load.bash'
load '/opt/bats-test-helpers/lox-bats-mock/stub.bash'


@test "clean_string function should should remove CR" {
  source /code/funcs.sh
  str=$(printf " test \n ")
  run clean_string $str
  [ "$status" -eq 0 ]
  assert_output "test"
}

@test "clean_string function should should remove spaces" {
  source /code/funcs.sh
  run clean_string "  test  "
  [ "$status" -eq 0 ]
  assert_output "test"
}

# @test "func1 function should return 2" {
#   source /code/example1.sh
#   run func1
#   [ "$status" -eq 2 ]
# }