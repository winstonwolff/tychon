#! /usr/bin/env python3

import sys
import _parser
import _builtins
from _builtins import Scope, evaluate
from os import path

PRELUDE_TY = path.join(path.dirname(path.realpath(__file__)), 'prelude.ty')

def _scope_with_prelude():
    scope = Scope(_builtins.BUILTIN_FUNCTIONS)
    scope.update({'stdout': sys.stdout})

    with open(PRELUDE_TY, 'rt') as f:
        prelude_str = f.read()
        result = evaluate(scope, _parser.parse(prelude_str))

    return scope

def _run_string(scope, code_str):
    ast = _parser.parse(code_str)
    result = evaluate(scope, ast)
    return (scope, result)

def _run_file(source_fname):
    scope = _scope_with_prelude()
    with open(source_fname, 'rt') as f:
        code_str = f.read()

        scope, result = _run_string(scope, code_str)

def _repl():
    print('Tython REPL')
    scope = _scope_with_prelude()
    try:
        while True:
            code_line = input('>>> ')
            scope, result = _run_string(scope, code_line)
            print(repr(result))
    except EOFError:
        print()
        return


def main():
    if len(sys.argv) > 1:
        source_fname = sys.argv[1]
        _run_file(source_fname)

    else:
        _repl()


if __name__ == '__main__':
    main()

