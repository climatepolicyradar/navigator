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


get_major() {
    echo "${1}" | cut -d'.' -f1
}

get_minor() {
    echo "${1}" | cut -d'.' -f2
}

get_patch() {
    echo "${1}" | cut -d'.' -f3 | cut -d'-' -f1
}

get_maturity() {
    echo "${1}" | cut -d'.' -f3 | cut -d'-' -f2
}