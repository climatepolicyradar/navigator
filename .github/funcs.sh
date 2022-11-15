#
# This is the core functionality taken out so it can be tested
#

clean_string() {
    echo "$1" | tr -d '\n' | tr -d ' '
}