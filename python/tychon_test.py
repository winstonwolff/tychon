import io
import tychon
from _util import trim_margin
import tempfile

def testing_scope():
    scope = tychon._scope_with_prelude()
    out = io.StringIO()
    scope.update({'stdout': out})
    return [scope, out]

def test_hello_world():
    scope, out = testing_scope()
    tychon.run_string("print('hello' 'world')", scope)
    assert out.getvalue() == 'hello world\n'

def test_inline_addition():
    scope, out = testing_scope()
    tychon.run_string("print(1 + 2)", scope)
    assert out.getvalue() == '3\n'

def test_evaulating_a_symbol():
    scope, out = testing_scope()
    tychon.run_string(trim_margin("""
        define(a 123)
        print(a)
        """), scope)
    assert out.getvalue() == '123\n'

#
# calling functions
#

def test_function_calling_function():
    scope, out = testing_scope()
    tychon.run_string("print( 'the sum is' add(3 4) )", scope)
    assert out.getvalue() == 'the sum is 7\n'

def test_double_colon_function_syntax():
    scope, out = testing_scope()
    tychon.run_string(trim_margin("""
        print ::
            'the sum is'
            add(3 4)
        """), scope)
    assert out.getvalue() == 'the sum is 7\n'

def test_defining_a_function():
    scope, out = testing_scope()
    tychon.run_string(trim_margin("""
        func(foo [a b] [a + b])
        print('foo(1 2) =' foo(1 2))
        """), scope)
    assert out.getvalue() == 'foo(1 2) = 3\n'

def test_defining_a_fuction_vertically():
    scope, out = testing_scope()
    tychon.run_string(trim_margin("""
        func ::
            foo
            a b
            [ a + b ]
        print('foo(1 2) =' foo(1 2))
        """), scope)
    assert out.getvalue() == 'foo(1 2) = 3\n'

#
# IF macro
#

def test_if():
    scope, out = testing_scope()
    tychon.run_string(trim_margin("""
        if(equal(1 2) print('yeah') print('nope'))
        """), scope)
    assert out.getvalue() == 'nope\n'

def test_if_as_expression():
    scope, out = testing_scope()
    tychon.run_string(trim_margin("""
        print(if(equal(1 2) 'yeah' 'nope'))
        """), scope)
    assert out.getvalue() == 'nope\n'

#
# Macros
#

def test_defining_macro():
    scope, out = testing_scope()
    tychon.run_string(trim_margin("""
        macro(debug_print [sym] [print(sym '=' evaluate(sym))])
        define(a 333)
        debug_print(a)
        """), scope)
    assert out.getvalue() == 'a = 333\n'

def test_define_function():
    scope, out = testing_scope()
    tychon.run_string(trim_margin("""
        func :: define_var [name value scope]
            dictionary_set(scope name value)
        define_var('k' 321 __scope__)

        print('the var k=' k)
        """), scope)
    assert out.getvalue() == 'the var k= 321\n'
