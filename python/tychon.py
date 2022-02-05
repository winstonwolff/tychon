#! /usr/bin/env python3

import sys
import _parser
import _builtins
from _builtins import Scope, evaluate

def run_string(code_line, stdout):
    ast = _parser.parse(code_line)
    scope = Scope(_builtins.BUILTIN_FUNCTIONS)
    scope.update({'stdout': stdout})
    return evaluate(scope, ast)

def _run_file(source_fname):
    with open(source_fname, 'rt') as f:
        code_str = f.read()

    for code_line in code_str.split('\n'):
        run_string(code_line, sys.stdout)

def _repl(stdin, stdout):
    print('Tython REPL')

    try:
        while True:
            code_line = input('>>> ')
            result = run_string(code_line, sys.stdout)
            print(repr(result))
    except EOFError:
        print()
        return


def main():
    if len(sys.argv) > 1:
        source_fname = sys.argv[1]
        _run_file(source_fname)

    else:
        _repl(sys.stdin, sys.stdout)


if __name__ == '__main__':
    main()

