#
# This is the core functionality taken out so it can be tested
#

clean_string() {
    echo "$1" | tr -d '\n' | tr -d ' '
}

is_tagged_version() {
    if [[ "$1" =~ refs/tags/v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)  ]]
    then
        return 0
    else
        return 1
    fi
}