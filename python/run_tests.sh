#!/usr/bin/env bash
set -x

# pytest options:
#       -k _ — only run tests with pattern of _, e.g. -k 'multiply or operator'

python3 -m pytest -vv --log-format="%(message)s"\
  --tb=native \
  --capture=no \
  _parser.py \
  _parser_test.py \
  _evaluator.py \
  tychon_test.py $1 $2 $3 $4

tychon dictionary.test.ty
tychon export_test.ty
