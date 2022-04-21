import io
import tychon
from _util import trim_margin


def test_hello_world():
    out = io.StringIO()
    tychon.run_string("print('hello' 'world')", out)
    assert out.getvalue() == 'hello world\n'

def test_inline_addition():
    out = io.StringIO()
    tychon.run_string("print(1 + 2)", out)
    assert out.getvalue() == '3\n'

def test_evaulating_a_symbol():
    out = io.StringIO()
    tychon.run_string(trim_margin("""
        define(a 123)
        print(a)
        """), out)
    assert out.getvalue() == '123\n'

#
# calling functions
#

def test_function_calling_function():
    out = io.StringIO()
    tychon.run_string("print( 'the sum is' add(3 4) )", out)
    assert out.getvalue() == 'the sum is 7\n'

def test_double_colon_function_syntax():
    out = io.StringIO()
    tychon.run_string(trim_margin("""
        print ::
            'the sum is'
            add(3 4)
        """), out)
    assert out.getvalue() == 'the sum is 7\n'

def test_defining_a_function():
    out = io.StringIO()
    tychon.run_string(trim_margin("""
        func(foo [a b] [a + b])
        print('foo(1 2) =' foo(1 2))
        """), out)
    assert out.getvalue() == 'foo(1 2) = 3\n'

def test_defining_a_fuction_vertically():
    out = io.StringIO()
    tychon.run_string(trim_margin("""
        func ::
            foo
            a b
            [ a + b ]
        print('foo(1 2) =' foo(1 2))
        """), out)
    assert out.getvalue() == 'foo(1 2) = 3\n'

#
# IF macro
#

def test_if():
    out = io.StringIO()
    tychon.run_string(trim_margin("""
        if(equal(1 2) print('yeah') print('nope'))
        """), out)
    assert out.getvalue() == 'nope\n'

def test_if_as_expression():
    out = io.StringIO()
    tychon.run_string(trim_margin("""
        print(if(equal(1 2) 'yeah' 'nope'))
        """), out)
    assert out.getvalue() == 'nope\n'

#
# Macros
#

def test_defining_macro():
    out = io.StringIO()
    tychon.run_string(trim_margin("""
        macro(debug_print [sym] [print(sym '=' evaluate(sym))])
        define(a 333)
        debug_print(a)
        """), out)
    assert out.getvalue() == 'a = 333\n'
