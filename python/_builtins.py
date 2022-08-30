import collections
import _parser
from pprint import pformat

#  QUIET = True
QUIET = False

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

def Scope(parent):
    if isinstance(parent, collections.ChainMap):
        return parent.new_child()
    else:
        return collections.ChainMap(parent)

class Kinds:
    FUNC = 'FUNC'
    MACRO = 'MACRO'


def _debug(scope, *args):
    '''debug level logging for Evaluator'''
    if QUIET: return
    indent = '    ' * scope['_depth']
    msg = '    ' + indent + ' '.join(str(a) for a in args)
    print(_Ansi.PURPLE, msg, _Ansi.RESET, sep='')


def evaluate(scope, expression):
    '''
    Execute some code.

    scope = modified in place
    expression = an AST node, or a list of nodes
    '''
    result = None

    if isinstance(expression, (str, int, float)):
        result = expression

    elif isinstance(expression, _parser.Sym) and expression.name=='__scope__':
        result = scope
        #  print('!!! eval:', repr(expression), '->', repr(result))
        _debug(scope, 'eval:', repr(expression), '->', repr(result))

    elif isinstance(expression, _parser.Sym):
        result = scope[expression.name]
        _debug(scope, 'eval:', repr(expression), '->', repr(result))

    elif isinstance(expression, _parser.Call):
        _debug(scope, 'eval:', repr(expression))
        scope['_depth'] += 1
        func_name = expression.function_name
        func = scope[func_name]
        args = expression.args

        if func.kind == Kinds.FUNC:
            _debug(scope, 'evaluating args since its a function')
            args = [evaluate(scope, arg) for arg in args]

        result = func(scope, *args)
        #  _debug(scope, '->', repr(result))
        scope['_depth'] -= 1
        result = result
        _debug(scope, 'eval:', '->', repr(result))

    elif isinstance(expression, (list, tuple)):
        if len(expression) != 0: _debug(scope, 'eval:', repr(expression))
        scope['_depth'] += 1
        result = tuple(evaluate(scope, e) for e in expression)
        scope['_depth'] -= 1
        if len(expression) != 0: _debug(scope, 'eval:', repr(result))

    else:
        result = expression

    #  if show_debug: _debug(scope, 'eval:', repr(expression), '->', repr(result))
    return result

#
#   Decorators
#

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

def doc(doc_str):
    def inside(decorated_value):
        decorated_value.__doc__ = doc_str
        return decorated_value
    return inside
#
#   Language features
#

@_builtin_function_with_name('pass')
def _pass(scope, args):
    pass

@_builtin_function
def parse(scope, code_str):
    ast = _parser.parse(code_str)
    return ast

@_builtin_function_with_name('evaluate')
def _evaluate(scope, ast):
    '''Executes the AST given'''
    return evaluate(scope, ast)

@builtin_macro
def define(scope, key_sym, value):
    _debug(scope, 'defining:', repr(key_sym), '=', repr(value))
    #  scope[key_sym.name] = value
    scope[key_sym.name] = evaluate(scope, value)
    return value

@builtin_macro
def define_no_eval(scope, key_sym, value):
    _debug(scope, 'defining no eval:', repr(key_sym), '=', repr(value))
    #  scope[key_sym.name] = value
    scope[key_sym.name] = value
    return value

@builtin_macro
def func(scope, func_name, arg_syms, program):

    class Func:
        kind = Kinds.FUNC
        def __call__(self, scope, *args):
            sub_scope = Scope(scope)
            sub_scope['__scope__'] = sub_scope

            # bind args to names
            for sym, arg in zip(arg_syms, args):
                define(sub_scope, sym, arg)

            results = evaluate(sub_scope, program)
            return results[-1] # just the last line's result

        def __repr__(self):
            arg_repr = ' '.join(str(a) for a in arg_syms)
            return f'<func {func_name}({arg_repr})>'
    new_function = Func()

    define(scope, func_name, new_function)
    return new_function

@builtin_macro
def macro(scope, macro_name, arg_syms, program):

    class Macro:
        kind = Kinds.MACRO
        def __call__(self, scope, *args):
            sub_scope = Scope(scope)
            sub_scope['__scope__'] = sub_scope

            # bind args to names
            for sym, arg in zip(arg_syms, args):
                define_no_eval(sub_scope, sym, arg)

            return evaluate(sub_scope, program)

        def __repr__(self):
            arg_repr = ' '.join(str(a) for a in arg_syms)
            return f'<macro {macro_name}({arg_repr})>'
    new_macro = Macro()

    define(scope, macro_name, new_macro)
    return new_macro

@macro_with_name('if')
def _if(scope, predicate, true_program, false_program=[]):
    test = evaluate(scope, predicate)

    if test:
        result = evaluate(scope, true_program)
    else:
        result = evaluate(scope, false_program)
    return result

#
#   List
#


@_builtin_function
@doc('returns a value inside `list` at `index`')
def list_get(scope, the_list, index):
    return the_list[index]

@_builtin_function
@doc('returns number of elements in `the_list`')
def list_length(scope, the_list):
    return len(index)

@_builtin_function
@doc('returns a new list containing `the_list` plus `new_value`')
def list_append(scope, the_list, new_value):
    return the_list + (new_value,)

#
#   Dictionary
#

@_builtin_function
@doc('create a new dictionary')
def dictionary(scope, *initial_items):
    return dict(initial_items)

@_builtin_function
@doc('returns item `key` from `the_dict`')
def dictionary_get(scope, the_dict, key):
    return the_dict[key]

@_builtin_function
@doc('Mutates `the_dict` by setting `key` to `value`')
def dictionary_set(scope, the_dict, key, value):
    the_dict[key] = value
    return value

#
#   Objects
#

@_builtin_function_with_name('getattr')
def _getattr(scope, object, attribute):
    return getattr(object, attribute)

#
#   File IO
#

@_builtin_function_with_name('print')
def _print(scope, *args, sep=' ', end="\n"):
    msg = sep.join(str(a) for a in args)
    scope['stdout'].write(msg)
    scope['stdout'].write(end)
    scope['stdout'].flush()

@_builtin_function
def file_read(scope, filename):
    with open(filename) as f:
        return f.read()

@_builtin_function
def file_open(scope, filename):
    return open(filename, 'w')

@_builtin_function
def file_close(scope, file_handle):
    file_handle.close

@_builtin_function
def file_write(scope, file_handle, *args, sep=' ', end="\n"):
    msg = sep.join(str(a) for a in args)
    file_handle.write(msg)
    file_handle.write(end)
    file_handle.flush()


#
#   Math
#

@_builtin_function
def add(scope, a, b):
    return a + b

@_builtin_function
def subtract(scope, a, b):
    return a - b

@_builtin_function
def multiply(scope, a, b):
    return a * b

@_builtin_function
def divide(scope, a, b):
    return a / b

@_builtin_function
def equal(scope, a, b):
    return a == b

#
#   scope
#

@_builtin_function
def scope(scope):
    '''Returns current scope as a formatted string'''
    return pformat(scope)

@_builtin_function
def rand_int(scope, low, high):
    '''Returns random integer between "low" and "high"'''
    import random
    return random.randint(low, high)

