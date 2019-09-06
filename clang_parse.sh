#!/usr/bin/env bash

# for Mac OS X
# brew install llvm
# pip install clang
export LD_LIBRARY_PATH="/usr/local/opt/llvm/lib:$LD_LIBRARY_PATH"

# for ubuntu
# pip3 install clang-5
export LD_LIBRARY_PATH="/usr/lib/llvm-5.0/lib:$LD_LIBRARY_PATH"

./clang_parse.py "$@"
