import collections

import _parser

class Kinds:
    FUNC = 'FUNC'
    MACRO = 'MACRO'

debug_verbose = False

def Scope(parent):
    if isinstance(parent, collections.ChainMap):
        return parent.new_child()
    else:
        return collections.ChainMap(parent)


def evaluate(scope, expression, verbose=None):
    '''
    Execute some code.

    scope = modified in place
    expression = an AST node, or a list of nodes
    '''
    result = None

    if verbose is not None:
        global debug_verbose
        debug_verbose = verbose

    if isinstance(expression, (str, int, float)):
        result = expression

    elif isinstance(expression, _parser.Sym) and expression.name=='__scope__':
        result = scope
        _debug(scope, 'eval:', repr(expression), '->', repr(result))

    elif isinstance(expression, _parser.Sym):
        result = scope[expression.name]
        _debug(scope, 'eval:', repr(expression), '->', repr(result))

    elif isinstance(expression, _parser.Call):
        _debug(scope, 'eval:', repr(expression))
        scope['_debug_print_depth'] += 1
        func_name = expression.function_name
        func = scope[func_name]
        args = expression.args

        if func.kind == Kinds.FUNC:
            _debug(scope, 'evaluating args since its a function')
            args = [evaluate(scope, arg) for arg in args]

        result = func(scope, *args)
        #  _debug(scope, '->', repr(result))
        scope['_debug_print_depth'] -= 1
        result = result
        _debug(scope, 'eval:', '->', repr(result))

    elif isinstance(expression, (list, tuple)):
        if len(expression) != 0: _debug(scope, 'eval:', repr(expression))
        scope['_debug_print_depth'] += 1
        result = tuple(evaluate(scope, e) for e in expression)
        scope['_debug_print_depth'] -= 1
        if len(expression) != 0: _debug(scope, 'eval:', repr(result))

    else:
        result = expression

    return result

def _debug(scope, *args):
    '''debug level logging for Evaluator'''
    if not debug_verbose: return
    indent = '    ' * scope['_debug_print_depth']
    msg = '    ' + indent + ' '.join(str(a) for a in args)
    print(_Ansi.PURPLE, msg, _Ansi.RESET, sep='')


class _Ansi:
    RESET = '\x1b[0m'
    GRAY  = '\x1b[90m'
    PURPLE= '\x1b[95m'
    RED   = '\x1b[31m'
    GREEN = '\x1b[32m'
    BLUE  = '\x1b[34m'
    CYAN  = '\x1b[36m'
