import sys
import parser

def run(code_str, stdout):

    ast = parser.parse(code_str)
    scope = Scope({**BUILTIN_FUNCTIONS, **{'stdout': stdout}})
    scope.run(ast)
    print('DONE. scope=', scope)

#  def main():
#      source_fname = sys.argv[1]
#      with open(source_fname, 'r') as f:
#          program = yaml.safe_load(f)

#      scope = Scope(BUILTIN_FUNCTIONS)
#      scope.run(program)
#      print('DONE. scope=', scope)

#  class Ansi:
#      RESET = '\x1b[0m'
#      GRAY  = '\x1b[90m'
#      RED   = '\x1b[31m'
#      GREEN = '\x1b[32m'
#      BLUE  = '\x1b[34m'
#      CYAN  = '\x1b[36m'


class Scope(dict):
    '''
    A dictionary that also has a `parent`. If you get an item which
    is not in this dictionary, the parent dictionary will be checked.
    '''
    def __init__(self, parent, initialize={}):
        super()
        self._parent = parent
        self.update(initialize)
        self._depth = parent._depth + 1 if isinstance(parent, Scope) else 0

    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        else:
            return self._parent[key]

    def debug(self, *args):
        indent = '    ' * self._depth
        msg = indent + ' '.join(str(a) for a in args)
        print(Ansi.GRAY, msg, Ansi.RESET, sep='')

    #  def info(self, *args):
    #      indent = '    ' * self._depth
    #      msg = indent + ' '.join(str(a) for a in args)
    #      print(Ansi.CYAN, msg, Ansi.RESET, sep='')

    def _evaluate(self, expression):
        print('!!! _evaluate() expression=', expression)
        if not isinstance(expression, list):
            # it's not a function call, so just return itself
            return expression

        self._depth += 1
        self.debug('eval:', repr(expression))
        func_name = expression[0]
        func = self[func_name]
        args = expression[1:]
        kind = getattr(func, 'kind', None)

        if kind == Kinds.FUNC:
            # It's a function call. Evaluate all args in turn
            args = [self._evaluate(arg) for arg in args]

        result = func(self, *args)
        self.debug('   ->', result)
        self._depth -= 1
        return result

    def run(self, program):
        result = None
        for expression in program:
            print('!!! run() expression=', expression)
            result = self._evaluate(expression)
        return result

BUILTIN_FUNCTIONS = {
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
    scope.stdout.write(msg)
    scope.stdout.write(end)
    scope.stdout.flush()
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
        result = sub_scope.run(true_program)
    else:
        result = sub_scope.run(false_program)
    return result


