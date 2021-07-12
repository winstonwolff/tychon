BUILTIN_FUNCTIONS = {
    '_depth': 0,
}

class Kinds:
    FUNC = 'FUNC'
    MACRO = 'MACRO'

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
def define(scope, key, value):
    scope[key] = value
    return value

@function
def get(scope, key):
    return scope[key]

@function_with_name('print')
def _print(scope, *args, sep=' ', end="\n"):
    msg = sep.join(str(a) for a in args)
    scope['stdout'].write(msg)
    scope['stdout'].write(end)
    scope['stdout'].flush()
    print("!!! msg=", msg)
    return msg

@macro
def defn(scope, func_name, arg_names, program):

    class Func:
        def __call__(self, scope, *args):
            sub_scope = Scope(scope)

            # bind args to names
            names_and_args = zip(arg_names, args)
            for name, arg in names_and_args:
                define(sub_scope, name, arg)

            return sub_scope.run(program)

        def __repr__(self):
            arg_repr = ' '.join(arg_names)
            return f'<function {func_name}({arg_repr})>'
    func = Func()

    define(scope, func_name, func)
    return func

@macro_with_name('if')
def _if(scope, predicate, true_program, false_program=[]):
    sub_scope = Scope(scope)

    test = sub_scope._evaluate(predicate)

    if test:
        result = Tychon.run(true_program)
    else:
        result = Tychon.run(false_program)
    return result


