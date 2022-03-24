#!/usr/bin/env bash
set -x

# pytest options:
#       -k _ — only run tests with pattern of _, e.g. -k 'multiply or operator'

python3 -m pytest --capture=no -vv \
  _parser.py \
  _parser_test.py \
  tychon_test.py $1 $2 $3 $4

