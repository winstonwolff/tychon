#! /usr/bin/env python3

import sys
import _parser
import _builtins
from _builtins import Scope, Evaluator
from pprint import pformat

def run(code_str, stdout):

    for code_line in code_str.split('\n'):
        #  print('!!! code_line=', code_line)
        ast = _parser.parse(code_line)
        #  print('!!! ast=', pformat(ast))
        scope = Scope(_builtins.BUILTIN_FUNCTIONS)
        scope.update({'stdout': stdout})
        Evaluator.run(scope, ast)
    #  print('DONE. scope=', scope)

def main():
    #  print('!!! sys.argv=', sys.argv)
    source_fname = sys.argv[1]
    with open(source_fname, 'rt') as f:
        code_str = f.read()
        run(code_str, sys.stdout)


if __name__ == '__main__':
    main()

