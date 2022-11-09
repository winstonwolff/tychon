from pprint import pformat
from immutables import Map
from collections import namedtuple

import _parser
from _evaluator import Kinds, Scope, evaluate, _debug
from _constants import Ansi

exports = {
    '_debug_print_depth': 0,
    'ANSI_RESET': Ansi.RESET,
    'ANSI_RED': Ansi.RED,
    'ANSI_GREEN': Ansi.GREEN,
    'ANSI_GRAY': Ansi.GRAY,
}


#
#   Decorators for exposing python functions and macros to Tychon
#

def _register(callable, name, kind):
    '''adda a function or macro to the list of BUILTINs'''
    callable.kind = kind
    exports[name] = callable


def tychon_function(func):
    '''
    Decorator for registering functions.

    When functions are called, their arguments are evaluated before passing in.
    '''
    _register(func, func.__name__, Kinds.FUNC)
    return func

def tychon_function_named(name):
    def inside(func):
        _register(func, name, Kinds.FUNC)
    return inside

def tychon_macro(func):
    '''
    Decorator for registering macros.

    When Macros are called, their arguments are not evaluated--the data structure
    is passed in to the macro as-is.
    '''
    _register(func, func.__name__, Kinds.MACRO)
    return func

def tychon_macro_named(name):
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

@tychon_function_named('pass')
def _pass(scope, args):
    pass

@tychon_function
def parse(scope, code_str):
    ast = _parser.parse(code_str)
    return ast

@tychon_function_named('evaluate')
def _evaluate(scope, ast):
    '''Executes the AST given'''
    return evaluate(scope, ast)

@tychon_macro
def define(scope, key_sym, value):
    _debug(scope, 'defining:', repr(key_sym), '=', repr(value))
    result = evaluate(scope, value)
    scope[key_sym.name] = result
    return result

@tychon_macro
def define_no_eval(scope, key_sym, value):
    _debug(scope, 'defining no eval:', repr(key_sym), '=', repr(value))
    scope[key_sym.name] = value
    return value

@tychon_macro
def func(scope, func_sym, arg_syms, program):

    class Func:
        kind = Kinds.FUNC
        __name__ = func_sym.name
        def __call__(self, scope, *args):
            sub_scope = Scope(scope)

            # bind args to names
            for sym, arg in zip(arg_syms, args):
                define(sub_scope, sym, arg)

            results = evaluate(sub_scope, program)
            return results[-1] # just the last line's result

        def __repr__(self):
            arg_repr = ' '.join(str(a) for a in arg_syms)
            return f'<func {func_sym.name}({arg_repr})>'
    new_function = Func()

    define(scope, func_sym, new_function)
    return new_function

@tychon_macro
def macro(scope, macro_name, arg_syms, program):

    class Macro:
        kind = Kinds.MACRO
        __name__ = macro_name
        def __call__(self, scope, *args):
            new_scope = Scope(scope)
            new_scope['caller_scope'] = scope

            # bind args to names
            for sym, arg in zip(arg_syms, args):
                define_no_eval(new_scope, sym, arg)

            return evaluate(new_scope, program)

        def __repr__(self):
            arg_repr = ' '.join(str(a) for a in arg_syms)
            return f'<macro {macro_name}({arg_repr})>'
    new_macro = Macro()

    define(scope, macro_name, new_macro)
    return new_macro

@tychon_macro_named('if')
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


@tychon_function
@doc('returns a value inside `list` at `index`')
def list_get(scope, the_list, index):
    return the_list[index]

@tychon_function
@doc('returns number of elements in `the_list`')
def list_length(scope, the_list):
    return len(index)

@tychon_function
@doc('returns a new list containing `the_list` plus `new_value`')
def list_append(scope, the_list, new_value):
    return the_list + (new_value,)

#
#   Immutable Dictionary
#

@tychon_function
@doc('create a new dictionary')
def Dictionary(scope, *initial_items):
    return Map(initial_items)

@tychon_function
@doc('returns item `key` from `the_dict`')
def dictionary_get(scope, the_dict, key):
    return the_dict[key]

@tychon_function
@doc('Returns a new immutable Dictionary with `key` set to `value`')
def dictionary_set(scope, the_dict, key, value):
    return the_dict.set(key, value)

@tychon_function
def dictionary_in(scope, the_dict, key):
    return key in the_dict

@tychon_function
def dictionary_keys(scope, the_dict):
    return list(the_dict.keys())

#
#   MutDictionary
#

@tychon_function
@doc('create a new mutable dictionary')
def MutDictionary(scope, *initial_items):
    return dict(initial_items)

@tychon_function
@doc('Modifies mutable Dictionary, setting `key` to `value`')
def mut_dictionary_set(scope, mut_dict, key, value):
    mut_dict[key] = value


#
#   Objects
#

@tychon_function_named('getattr')
def _getattr(scope, object, attribute):
    return getattr(object, attribute)

#
#   File IO
#

@tychon_function_named('print')
def _print(scope, *args, sep=' ', end="\n"):
    msg = sep.join(str(a) for a in args)
    scope['stdout'].write(msg)
    scope['stdout'].write(end)
    scope['stdout'].flush()

@tychon_function
def file_read(scope, filename):
    with open(filename) as f:
        return f.read()

@tychon_function
def file_open(scope, filename):
    return open(filename, 'w')

@tychon_function
def file_close(scope, file_handle):
    file_handle.close

@tychon_function
def file_write(scope, file_handle, *args, sep=' ', end="\n"):
    msg = sep.join(str(a) for a in args)
    file_handle.write(msg)
    file_handle.write(end)
    file_handle.flush()


#
#   Math
#

@tychon_function
def add(scope, a, b):
    return a + b

@tychon_function
def subtract(scope, a, b):
    return a - b

@tychon_function
def multiply(scope, a, b):
    return a * b

@tychon_function
def divide(scope, a, b):
    return a / b

#
#   Comparison and Logic
#

@tychon_function
def equal(scope, a, b):
    return a == b

@tychon_function_named('not')
def _not(scope, a):
    return not a

#
#   other
#

@tychon_function
def rand_int(scope, low, high):
    '''Returns random integer between "low" and "high"'''
    import random
    return random.randint(low, high)

