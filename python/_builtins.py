import collections
import _parser
from pprint import pformat

class _Ansi:
    RESET = '\x1b[0m'
    GRAY  = '\x1b[90m'
    PURPLE= '\x1b[95m'
    RED   = '\x1b[31m'
    GREEN = '\x1b[32m'
    BLUE  = '\x1b[34m'
    CYAN  = '\x1b[36m'


BUILTIN_FUNCTIONS = {
    '_depth': 0,
}

def Scope(parent, initialize={}):
    if isinstance(parent, collections.ChainMap):
        return parent.new_child()
    else:
        return collections.ChainMap(parent)

class Kinds:
    FUNC = 'FUNC'
    MACRO = 'MACRO'


def _debug(scope, *args):
    '''debug level logging for Evaluator'''
    indent = '    ' * scope['_depth']
    msg = '    ' + indent + ' '.join(str(a) for a in args)
    print(_Ansi.PURPLE, msg, _Ansi.RESET, sep='')


def evaluate(scope, expression):
    '''
    Execute some code.

    expression = an AST node, or a list of nodes
    '''
    result = None
    show_debug = True

    if isinstance(expression, (str, int, float)):
        result = expression
        show_debug = False

    elif isinstance(expression, _parser.Sym):
        result = scope[expression.name]

    elif isinstance(expression, _parser.Call):
        scope['_depth'] += 1
        func_name = expression[0].name
        func = scope[func_name]
        args = expression[1:]

        if func.kind == Kinds.FUNC:
            args = [evaluate(scope, arg) for arg in args]

        result = func(scope, *args)
        #  _debug(scope, '->', repr(result))
        scope['_depth'] -= 1
        result = result

    elif isinstance(expression, (list, tuple)):
        result = tuple(evaluate(scope, e) for e in expression)[-1]
    else:
        result = expression

    if show_debug: _debug(scope, 'eval:', repr(expression), '->', repr(result))
    return result


def _register(callable, name, kind):
    '''adda a function or macro to the list of BUILTINs'''
    callable.kind = kind
    BUILTIN_FUNCTIONS[name] = callable


def _builtin_function(func):
    '''
    Decorator for registering functions.

    When functions are called, their arguments are evaluated before passing in.
    '''
    _register(func, func.__name__, Kinds.FUNC)
    return func

def _builtin_function_with_name(name):
    def inside(func):
        _register(func, name, Kinds.FUNC)
    return inside

def builtin_macro(func):
    '''
    Decorator for registering macros.

    When Macros are called, their arguments are not evaluated--the data structure
    is passed in to the macro as-is.
    '''
    _register(func, func.__name__, Kinds.MACRO)
    return func

def macro_with_name(name):
    def inside(func):
        _register(func, name, Kinds.MACRO)
    return inside

@_builtin_function_with_name('pass')
def _pass(scope, args):
    pass

@_builtin_function
def add(scope, a, b):
    return a + b

@_builtin_function
def equal(scope, a, b):
    return a == b

@_builtin_function
def scope(scope):
    '''Returns current scope as a formatted string'''
    return pformat(scope)

@builtin_macro
def define(scope, key_sym, value):
    #  value = Evaluate.run(scope, value)
    _debug(scope, 'defining:', repr(key_sym), '=', repr(value))
    scope[key_sym.name] = value
    return value

#  @_builtin_function
#  def get(scope, key_sym):
#      _debug(scope, 'getting:', repr(key_sym))
#      return scope[key_sym.name]

@_builtin_function_with_name('print')
def _print(scope, *args, sep=' ', end="\n"):
    msg = sep.join(str(a) for a in args)
    scope['stdout'].write(msg)
    scope['stdout'].write(end)
    scope['stdout'].flush()
    return msg

@builtin_macro
def func(scope, func_name, arg_syms, program):

    class Func:
        kind = Kinds.FUNC
        def __call__(self, scope, *args):
            sub_scope = Scope(scope)

            # bind args to names
            syms_and_args = zip(arg_syms, args)
            for sym, arg in syms_and_args:
                define(sub_scope, sym, arg)

            return evaluate(sub_scope, program)

        def __repr__(self):
            arg_repr = ' '.join(str(a) for a in arg_syms)
            return f'<function {func_name}({arg_repr})>'
    func = Func()

    define(scope, func_name, func)
    return func

@macro_with_name('if')
def _if(scope, predicate, true_program, false_program=[]):
    sub_scope = Scope(scope)

    test = evaluate(scope, predicate)

    if test:
        result = evaluate(scope, true_program)
    else:
        result = evaluate(scope, false_program)
    return result
