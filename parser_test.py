"""
to run tests:
    python3 -m pytest -v main.py
"""

import re
import pytest

from parser import parse

class Color:
    red = '\x1b[31m'
    green = '\x1b[32m'
    reset = '\x1b[39;49m'
    #  grey = '\x1b[90m'
    default = '\x1b[39m'

def trim_margin(str):
    '''Trim left margin of spaces. The last line is used to gauge how where the margin is.'''
    lines = str.split('\n')
    last_line = lines[-1]
    margin_width = len(last_line)
    lines = map(lambda l: l[margin_width:], lines)
    return '\n'.join(lines)

def test_trim_margin():
    str = '''
        abc
        def
        '''
    assert trim_margin(str) == '\nabc\ndef\n'

def without_parseinfo(node):
    if isinstance(node, dict) and 'parseinfo' in node:
        print(Color.default, '     node=', repr(node), Color.reset)
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
    if isinstance(tree, list):
        return list( map_tree(func, item) for item in tree)
    elif isinstance(tree, dict):
        return func( { k: map_tree(func, v ) for k, v in tree.items() } )
    else:
        return func(tree)

def test_list():
    assert map_tree(len, ['a', 'bb']) == [1, 2]
def test_deep_list():
    assert map_tree(len, ['a', ['b', 'c']]) == [1, [1, 1]]
def test_dict():
    assert map_tree(without_parseinfo, {'aa':'a', 'parseinfo':'PI'}) == {'aa': 'a'}
def test_deep_dict():
    assert map_tree(without_parseinfo, {'a':'aa', 'parseinfo': 'AA', 'b':{'c':'cc', 'parseinfo': 'CC'}}) == {'a': 'aa', 'b': {'c': 'cc'}}

EXAMPLES = (
    ('"hello"', [{'string': 'hello'}]),
    ('"hello my friend"', [ {'string': 'hello my friend'}]),
    ('foo', [{'identifier': 'foo'}]),
    ('123', [{'integer': '123'}]),
    ('123 456', [[{'integer': '123'}, {'integer': '456'}]]),
    ("123\n456", [{'integer': '123'}, {'integer': '456'}]),
    ('123.4', [{'float': '123.4'}]),
    ('add 1 2', [[{'identifier': 'add'}, {'integer': '1'}, {'integer': '2'}]]),
    ('2 + 3',  [{'op': '+', 'left': { 'integer': '2'}, 'right': {'integer': '3'}}]),
    ('3.14 * 2',  [{'op': '*', 'left': {'float': '3.14'}, 'right': {'integer': '2'}}]),
    ('2 + 3 * 4',  [
        {'op': '+',
         'left': {'integer': '2'},
         'right': {
             'op': '*',
             'left': {'integer': '3'},
             'right': {'integer': '4'}}}]),
    (trim_margin('''
        111
            222
            333
        444
        '''), [
        {'empty_line': '\n'},
        {'integer': '111'},
        {'vertical_list': [
            {'integer': '222'},
            {'integer': '333'},
        ]},
        {'integer': '444'},
    ]),
    ('add(1 2)',  [
        {
            'function_call': 'add',
            'args': [{'integer': '1'}, {'integer': '2'}]
        }
    ]),
    ('print("hello" "world")',  [
        {
            'function_call': 'print',
            'args': [{'string': 'hello'}, {'string': 'world'}]
        }
    ]),
)

@pytest.fixture(scope="module", params=EXAMPLES)
def example(request):
    return request.param

def test_parsing(example):
    source, expected = example
    actual = parse(source)
    actual = map_tree(without_parseinfo, actual)
    assert actual == expected

