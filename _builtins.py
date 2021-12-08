import collections
import _parser

class Ansi:
    RESET = '\x1b[0m'
    GRAY  = '\x1b[90m'
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

class Evaluator:

    @staticmethod
    def run(scope, program):
        result = None
        for expression in program:
            result = Evaluator._evaluate(scope, expression)
        return result

    @staticmethod
    def debug(scope, *args):
        indent = '    ' * scope['_depth']
        msg = indent + ' '.join(str(a) for a in args)
        print(Ansi.GRAY, msg, Ansi.RESET, sep='')

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
        Evaluator.debug(scope, 'eval:', repr(call))
        func_name = call[0].name
        func = scope[func_name]
        args = call[1:]
        #  kind = getattr(func, 'kind', None)

        args = [Evaluator._evaluate(scope, arg) for arg in args]

        result = func(scope, *args)
        Evaluator.debug(scope, '   ->', result)
        scope['_depth'] -= 1
        return result

def _register(func, name, kind):
    func.kind = kind
    BUILTIN_FUNCTIONS[name] = func


def function(func):
    '''
    Decorator for registering functions.

    When functions are called, their arguments are evaluated before passing in.
    '''
    _register(func, func.__name__, Kinds.FUNC)
    return func

def function_with_name(name):
    def inside(func):
        _register(func, name, Kinds.FUNC)
    return inside

def macro(func):
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

@function_with_name('pass')
def _pass(scope, args):
    pass

@function
def add(scope, a, b):
    return a + b

@function
def equal(scope, a, b):
    return a == b

@function
def define(scope, key_sym, value):
    Evaluator.debug(scope, 'define', repr(key_sym), '=', repr(value))
    scope[key_sym.name] = value
    return value

@function
def get(scope, key_sym):
    Evaluator.debug(scope, 'get', repr(key_sym))
    return scope[key_sym.name]

@function_with_name('print')
def _print(scope, *args, sep=' ', end="\n"):
    msg = sep.join(str(a) for a in args)
    scope['stdout'].write(msg)
    scope['stdout'].write(end)
    scope['stdout'].flush()
    return msg

@macro
def defn(scope, func_name, arg_syms, program):

    class Func:
        def __call__(self, scope, *args):
            sub_scope = Scope(scope)

            # bind args to names
            syms_and_args = zip(arg_syms, args)
            for sym, arg in syms_and_args:
                define(sub_scope, sym, arg)

            return Evaluator.run(sub_scope, program)

        def __repr__(self):
            arg_repr = ' '.join(str(a) for a in arg_syms)
            return f'<function {func_name}({arg_repr})>'
    func = Func()

    define(scope, func_name, func)
    return func

@macro_with_name('if')
def _if(scope, predicate, true_program, false_program=[]):
    sub_scope = Scope(scope)

    test = sub_scope._evaluate(predicate)

    if test:
        result = Evaluator.run(true_program)
    else:
        result = Evaluator.run(false_program)
    return result


