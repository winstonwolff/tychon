#! /usr/bin/env python3

import sys
import _parser
import _builtins
from _builtins import Scope, Evaluator
from pprint import pformat

def run_file(source_filename):

    with open(source_fname, 'rt') as f:
        code_str = f.read()

    for code_line in code_str.split('\n'):
        #  print('!!! code_line=', code_line)
        ast = _parser.parse(code_line)
        #  print('!!! ast=', pformat(ast))
        scope = Scope(_builtins.BUILTIN_FUNCTIONS)
        scope.update({'stdout': stdout})
        Evaluator.run(scope, ast)
    #  print('DONE. scope=', scope)

CTRL_D = '\0x4'
def repl(stdin, stdout):

    print('Tython REPL')

    try:
        while True:
            code_line = input('>>> ')

            ast = _parser.parse(code_line)
            scope = Scope(_builtins.BUILTIN_FUNCTIONS)
            scope.update({'stdout': stdout})
            result = Evaluator.run(scope, ast)
            print(repr(result))
    except EOFError:
        print()
        return


def main():
    #  print('!!! sys.argv=', sys.argv)
    if len(sys.argv) > 1:
        source_fname = sys.argv[1]
        run_file(source_fname)

    else:
        repl(sys.stdin, sys.stdout)


if __name__ == '__main__':
    main()

