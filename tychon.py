#! /usr/bin/env python3

import sys
import _parser
import _builtins
from _builtins import Scope, Evaluator
from pprint import pformat

def run(code_str, stdout):

    ast = _parser.parse(code_str)
    print('!!! ast=', pformat(ast))
    scope = Scope(_builtins.BUILTIN_FUNCTIONS)
    scope.update({'stdout': stdout})
    Evaluator.run(scope, ast)
    #  print('DONE. scope=', scope)

def main():
    source_fname = sys.argv[1]
    with open(source_fname, 'r') as f:
        code_str = f.read()
        run(code_str, sys.stdout)


if __name__ == '__main__':
    main()

