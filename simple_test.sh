#!/usr/bin/env bash

cmdcheck() { type >/dev/null 2>&1 "$@"; }

shopt -s expand_aliases
cmdcheck icdiff && diff() {
  icdiff -U 1 --line-numbers "$@"
}

test() {
  if [[ $# -lt 1 ]]; then
    command cat <<EOF 1>&2
$(basename "$0") <filepath>
EOF
    return 1
  fi

  local target_filepath="$1"
  local test_dir='.test'
  mkdir -p "$test_dir"
  cat "$target_filepath" | sed 's/[^a-zA-Z0-9_]/ /g' | tr ' ' '\n' | grep -i good >"$test_dir/required_good.log"
  cat "$target_filepath" | sed 's/[^a-zA-Z0-9_]/ /g' | tr ' ' '\n' | grep -i bad >"$test_dir/required_bad.log"
  ./clang_parse.sh "$target_filepath" | tee "$test_dir/out.log"
  cat "$test_dir/out.log" | sed 's/.*:[ ]*//g' | grep -i good >"$test_dir/got_good.log"
  cat "$test_dir/out.log" | sed 's/.*:[ ]*//g' | grep -i bad >"$test_dir/got_bad.log"

  local good_out
  good_out=$(diff <(:) "$test_dir/got_good.log")
  good_ret=$?
  [[ $good_ret != 0 ]] && echo "# good name result test\n$good_out"
  local bad_out
  bad_out=$(diff "$test_dir/required_bad.log" "$test_dir/got_bad.log")
  bad_ret=$?
  [[ $bad_ret != 0 ]] && echo "# bad name result test\n$bad_out"

  [[ $good_ret == 0 ]] && [[ $bad_ret == 0 ]]
  return
}

test "$@"
