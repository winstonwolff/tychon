#! /usr/bin/env python3

import sys
import collections
import _parser
import _builtins

def run(code_str, stdout):

    ast = _parser.parse(code_str)
    scope = Scope(_builtins.BUILTIN_FUNCTIONS)
    scope.update({'stdout': stdout})
    Tychon.run(scope, ast)
    #  print('DONE. scope=', scope)

def main():
    source_fname = sys.argv[1]
    with open(source_fname, 'r') as f:
        code_str = f.read()
        run(code_str, sys.stdout)

class Ansi:
    RESET = '\x1b[0m'
    GRAY  = '\x1b[90m'
    RED   = '\x1b[31m'
    GREEN = '\x1b[32m'
    BLUE  = '\x1b[34m'
    CYAN  = '\x1b[36m'


def Scope(parent):
    if isinstance(parent, collections.ChainMap):
        return parent.new_child(initialize)
    else:
        return collections.ChainMap(parent)


class Tychon:

    @staticmethod
    def run(scope, program):
        result = None
        for expression in program:
            result = Tychon._evaluate(scope, expression)
        return result

    @staticmethod
    def debug(scope, *args):
        indent = '    ' * scope['_depth']
        msg = indent + ' '.join(str(a) for a in args)
        #  print(Ansi.GRAY, msg, Ansi.RESET, sep='')

    @staticmethod
    def info(scope, *args):
        indent = '    ' * scope['_depth']
        msg = indent + ' '.join(str(a) for a in args)
        #  print(Ansi.CYAN, msg, Ansi.RESET, sep='')

    @staticmethod
    def _evaluate(scope, expression):
        if not isinstance(expression, _parser.Call):
            # it's not a function call, so just return itself
            return expression

        call = expression

        scope['_depth'] += 1
        Tychon.debug(scope, 'eval:', repr(call))
        func_name = call.args[0].name
        func = scope[func_name]
        args = call.args[1:]
        #  kind = getattr(func, 'kind', None)

        args = [Tychon._evaluate(scope, arg) for arg in args]

        result = func(scope, *args)
        Tychon.debug(scope, '   ->', result)
        scope['_depth'] -= 1
        return result

if __name__ == '__main__':
    main()

