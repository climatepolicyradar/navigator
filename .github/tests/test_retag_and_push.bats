#!/usr/bin/env bats

@test "docker_tag function should tag a as b" {
  alias docker=echo
  source /code/retag-and-push.sh
  run docker_tag a b
  [ "$output" -eq "Re-tagging a -> b" ]
}

# @test "func1 function should return 2" {
#   source /code/example1.sh
#   run func1
#   [ "$status" -eq 2 ]
# }