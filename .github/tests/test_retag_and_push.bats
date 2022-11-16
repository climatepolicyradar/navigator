#!/usr/bin/env bats
load '/opt/bats-test-helpers/bats-support/load.bash'
load '/opt/bats-test-helpers/bats-assert/load.bash'
load '/opt/bats-test-helpers/lox-bats-mock/stub.bash'

# ------

@test "clean_string removes CR" {
  source /code/funcs.sh
  str=$(printf " test \n ")
  run clean_string $str
  [ "$status" -eq 0 ]
  assert_output "test"
}

@test "clean_string removes all white spaces" {
  source /code/funcs.sh
  run clean_string "  test  "
  [ "$status" -eq 0 ]
  assert_output "test"
}

# ------

@test "is_tagged_version succeeds for typical version" {
  source /code/funcs.sh
  run is_tagged_version "refs/tags/v0.1.2-alpha"
  [ "$status" -eq 0 ]
}

@test "is_tagged_version fails for missing patch " {
  source /code/funcs.sh
  run is_tagged_version "refs/tags/v0.1-alpha"
  [ "$status" -eq 1 ]
}

@test "is_tagged_version fails for other tags " {
  source /code/funcs.sh
  run is_tagged_version "refs/tags/vimto"
  [ "$status" -eq 1 ]
}

# ------