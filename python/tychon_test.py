import io
import tychon

def test_hello_world():
    out = io.StringIO()
    tychon.run_string("print('hello' 'world')", out)
    assert out.getvalue() == 'hello world\n'

def test_inline_addition():
    out = io.StringIO()
    tychon.run_string("print(1 + 2)", out)
    assert out.getvalue() == '3\n'

def test_function_calling_function():
    out = io.StringIO()
    tychon.run_string("print( 'the sum is' add(3 4) )", out)
    assert out.getvalue() == 'the sum is 7\n'

def test_evaulating_a_symbol():
    out = io.StringIO()
    tychon.run_string("""
define(a 123)
print(a)""", out)
    assert out.getvalue() == '123\n'

def test_defining_a_fuction():
    out = io.StringIO()
    tychon.run_string("""
func(foo [a b] [a + b])
print('foo(1 2) =' foo(1 2))""", out)
    assert out.getvalue() == 'foo(1 2) = 3\n'

def test_if():
    out = io.StringIO()
    tychon.run_string("""
if(equal(1 2) print('yeah') print('nope'))
""", out)
    assert out.getvalue() == 'nope\n'

def test_if_is_expression():
    out = io.StringIO()
    tychon.run_string("""
print(if(equal(1 2) 'yeah' 'nope'))
""", out)
    assert out.getvalue() == 'nope\n'
