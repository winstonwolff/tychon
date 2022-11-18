import collections

from _constants import Ansi
import _parser

class Kinds:
    FUNC = 'FUNC'
    MACRO = 'MACRO'

debug_verbose = False

class TychonError(Exception): pass

def Scope(parent):
    if isinstance(parent, collections.ChainMap):
        return parent.new_child()
    else:
        return collections.ChainMap(parent).new_child()

def test_scope():
    one = Scope({'a': 1})
    one['aa'] = 22

    two = Scope(one)
    two['b'] = 33

    assert isinstance(one, collections.ChainMap)
    assert one.maps == [{'aa': 22}, {'a':1}]
    assert one['a'] == 1
    assert 'b' not in one

    assert isinstance(two, collections.ChainMap)
    assert two.maps == [{'b': 33}, {'aa': 22}, {'a':1}]
    assert two['a'] == 1
    assert two['b'] == 33


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

    try:

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

    except TychonError:
        raise
    except Exception as exc:
        if not hasattr(expression, 'parseinfo'):
            #  _error(scope, 'evaluate() exception but no parse info:', repr(exc))
            file_and_line = f'{repr(expression)} at unknown location'
        else:
            file_and_line = source_file_at(expression.parseinfo)
            #  _error(scope, 'evaluate() exception:',
            #     repr(exc),
            #     expression.parseinfo,
            #      file_and_line)
        raise TychonError(file_and_line) from exc

    return result

def source_file_at(parseinfo):
    line_info = parseinfo.tokenizer.line_info(parseinfo.pos)
    return f'{line_info.filename}:{line_info.line}:{line_info.col}\n    {line_info.text}'

def _debug(scope, *args):
    '''debug level logging for Evaluator'''
    if not debug_verbose: return
    indent = '    ' * (1 + scope['_debug_print_depth'])
    msg = indent + ' '.join(str(a) for a in args)
    print(Ansi.PURPLE, msg, Ansi.RESET, sep='')

#  def _error(scope, *args):
#      '''error level logging for Evaluator'''
#      indent = '    ' * (1 + scope['_debug_print_depth'])
#      msg = indent + ' '.join(str(a) for a in args)
#      print(Ansi.RED, msg, Ansi.RESET, sep='')
