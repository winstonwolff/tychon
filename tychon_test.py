import io
import tychon

def test_hello_world():
    out = io.StringIO()
    tychon.run("print('hello' 'world')", out)
    assert out.getvalue() == 'hello world\n'

def test_inline_addition():
    out = io.StringIO()
    tychon.run("print(1 + 2)", out)
    assert out.getvalue() == '3\n'

def test_function_calling_function():
    out = io.StringIO()
    tychon.run("print( 'the sum is' add(3 4) )", out)
    assert out.getvalue() == 'the sum is 7\n'


