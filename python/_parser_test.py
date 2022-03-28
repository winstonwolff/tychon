"""
to run tests:
    python3 -m pytest -v main.py
"""

import re
import pytest
from _util import trim_margin

from _parser import parse, Call, Sym

class Color:
    red = '\x1b[31m'
    green = '\x1b[32m'
    reset = '\x1b[39;49m'
    #  grey = '\x1b[90m'
    default = '\x1b[39m'

def without_parseinfo(node):
    if isinstance(node, dict) and 'parseinfo' in node:
        #  print(Color.default, '     node=', repr(node), Color.reset)
        return {k:v for k, v in node.items() if k != 'parseinfo'}
    else:
        return node

def test_without_parseinfo():
    node = {
        'value': 'EXAMPLE VALUE',
        'parseinfo': 'EXAMPLE PARSE INFO' }
    assert without_parseinfo(node) == {'value': 'EXAMPLE VALUE'}

def map_tree(func, tree):
    """Returns a tree in the same shape, but with each node mutated by 'func'"""
    if isinstance(tree, list) or isinstance(tree, tuple):
        return list( map_tree(func, item) for item in tree)
    elif isinstance(tree, dict):
        return func( { k: map_tree(func, v ) for k, v in tree.items() } )
    else:
        return func(tree)

def test_map_tree_string():
    assert map_tree(len, 'aaaa') == 4

def test_map_tree_list():
    assert map_tree(len, ['a', 'bb']) == [1, 2]

def test_map_tree_tuple():
    assert map_tree(len, ('a', 'bb')) == [1, 2]

def test_map_tree_deep_list():
    assert map_tree(len, ['a', ['b', 'c']]) == [1, [1, 1]]

def test_map_tree_dict():
    assert map_tree(without_parseinfo, {'aa':'a', 'parseinfo':'PI'}) == {'aa': 'a'}

def test_map_tree_deep_dict():
    assert map_tree(without_parseinfo, {'a':'aa', 'parseinfo': 'AA', 'b':{'c':'cc', 'parseinfo': 'CC'}}) == {'a': 'aa', 'b': {'c': 'cc'}}

def test_map_tree_parse_info_call():
    assert map_tree(without_parseinfo, Call([Sym('foo'), 33, 44])) == Call([Sym('foo'), 33, 44])


def parse_without_info(source):
    ast = parse(source)
    simpler_ast = map_tree(without_parseinfo, ast)
    return simpler_ast

#
# terms
#

def test_parse_string():
    assert parse_without_info('"hello"') == 'hello'

def test_parse_symbol():
    assert parse_without_info('foo') == Sym('foo')

def test_parse_integer():
    assert parse_without_info('123') == 123

def test_parse_float():
    assert parse_without_info('123.4') == 123.4

#
# lists
#

def test_parse_one_line_of_terms():
    assert parse_without_info('aaa 1.3 "string"') == [Sym('aaa'), 1.3, "string"]

def test_parse_bracket_list():
    assert parse_without_info('[123 456]') == [123, 456]

def test_parse_vertical_list():
    assert parse_without_info("123\n456") == [123, 456]

def test_parse_indented_lists():
    assert parse_without_info(trim_margin('''
        111
            222
            333 333
        444
        ''')) == [
            {'empty_line': '\n'},
            111,
            [
                222,
                [333, 333],
            ],
            444
        ]
# 
# traditional math syntax with binary operators
#

def test_parse_binary_operator():
    assert parse_without_info('foo 1 2') == [Sym('foo'), 1, 2]

def test_parse_multiply_operator():
    assert parse_without_info('3.14 * 2') ==  Call([ Sym('multiply'), 3.14, 2])

def test_parse_binary_operator_precedence():
    assert parse_without_info('2 + 3 * 4') == \
        Call([ Sym('add'), 2, Call([ Sym('multiply'), 3, 4])])

def test_parse_parenthesis():
    assert parse_without_info('(2 + 3) * 4') == \
        Call([ Sym('multiply'), Call([ Sym('add'), 2, 3]), 4])

#
# functions - calling and defining
#

def test_parse_function_call():
    assert parse_without_info('add(1 2)') == Call([Sym('add'), 1, 2])

def test_parse_colon_function_call():
    assert parse_without_info(trim_margin('''
        print ::
            "hello"
            "world"
        ''')) == [
            {'empty_line': '\n'},
            Call([ Sym('print'), "hello", "world"]),
        ]

def test_parse_colon_function_call_one_line():
    assert parse_without_info('print :: "hello" "world"') == Call(
        [ Sym('print'), "hello", "world"])

def test_parse_defining_function():
    assert parse_without_info('func(addition [a b] [a + b])') == Call([Sym('func'),
              Sym('addition'),
              [Sym('a'), Sym('b')],
              [Call([Sym('add'), Sym('a'), Sym('b')])]
             ])

def test_parse_define_function_vertical_syntax():
    assert parse_without_info(trim_margin('''
        func ::
            addition
            a b
            [ a + b ]
        ''')) == [
        {'empty_line': '\n'},
        Call([ Sym('func'),
               Sym('addition'),
               ( Sym('a'), Sym('b') ),
               [
                 Call([ Sym('add'), Sym('a'), Sym('b') ])
               ]
            ])
    ]

#
# Macros
#

def test_parse_define_macro():
    assert parse_without_info("macro(blah [] [])") == Call([Sym('macro'), Sym('blah'), [], [] ])

