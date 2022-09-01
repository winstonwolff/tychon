#! /usr/bin/env python3

import sys
import _parser
import _builtins
from _builtins import Scope
from _evaluator import evaluate
from os import path
import argparse

PRELUDE_TY = path.join(path.dirname(path.realpath(__file__)), 'prelude.ty')

def _scope_with_prelude():
    scope = Scope(_builtins.BUILTIN_FUNCTIONS)
    scope.update({'stdout': sys.stdout})

    with open(PRELUDE_TY, 'rt') as f:
        prelude_str = f.read()
        result = evaluate(scope, _parser.parse(prelude_str))

    return scope

def run_string(code_str, scope, verbose=None):
    scope = scope or _scope_with_prelude()
    ast = _parser.parse(code_str)
    result = evaluate(scope, ast, verbose)
    return (scope, result)

def _run_file(source_fname, verbose):
    scope = _scope_with_prelude()
    with open(source_fname, 'rt') as f:
        code_str = f.read()

        scope, result = run_string(code_str, scope=scope, verbose=verbose)

def _repl(verbose):
    print('Tython REPL')
    scope = _scope_with_prelude()
    try:
        while True:
            code_line = input('>>> ')
            scope, result = run_string(code_line, scope=scope, verbose=verbose)
            print(repr(result))
    except EOFError:
        print()
        return


def main():
    parser = argparse.ArgumentParser(description='Tychon interpreter and REPL.')
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument('tychon_source', nargs='*')
    args = parser.parse_args()

    if len(args.tychon_source) >= 1:
        source_fname = args.tychon_source[0]
        _run_file(source_fname, verbose=args.verbose)

    else:
        _repl(verbose)


if __name__ == '__main__':
    main()

