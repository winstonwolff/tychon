import io
import tempfile
from pprint import pformat

import tychon
from _util import trim_margin
from _parser import Call, Sym

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
#   Collections
#

def test_list_manipulation():
    scope, out = testing_scope()
    tychon.run_string(trim_margin("""
        define( lst [4 2 5 1] )
        print("list_length(lst)=" 4)
        print("list_get(lst, 2)=" list_get(lst, 2))

        define :: lst_2 list_append(lst 99)
        print("lst_2=" lst_2)
        """), scope)
    assert out.getvalue() == 'list_length(lst)= 4\nlist_get(lst, 2)= 5\nlst_2= (4, 2, 5, 1, 99)\n'

def test_dictionary_manipulation():
    scope, out = testing_scope()
    tychon.run_string(trim_margin("""
        define( d dictionary( ["a" 11] ["b" 22] ) )
        print("d=" d)
        print("dictionary_get( d 'b' )=" dictionary_get( d 'b' ))
        dictionary_set( d 'c' 33 )
        print("dictionary_get( d 'c' )=" dictionary_get( d 'c' ))
        """), scope)
    assert out.getvalue() == "d= {'a': 11, 'b': 22}\ndictionary_get( d 'b' )= 22\ndictionary_get( d 'c' )= 33\n"

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

def test_read_code():
    scope, out = testing_scope()

    with tempfile.NamedTemporaryFile(prefix='test_import', suffix='.ty') as temp_file:
        temp_file.write(trim_margin('''
            define(a 1)
            a + 33
            ''').encode())
        temp_file.flush()
        (out_scope, result) = tychon.run_string(f"read_code( '{temp_file.name}' )",
                                               scope)
        assert len(result) == 2
        assert result[0] == Call([ Sym('define'), Sym('a'), 1])
        assert result[1] == Call([ Sym('add'), Sym('a'), 33])

def test_lang_load_module():
    scope, out = testing_scope()

    with tempfile.NamedTemporaryFile(prefix='test_import', suffix='.ty') as temp_file:
        temp_file.write(trim_margin('''
            define(a 1)
            define(b 2)
            ''').encode())
        temp_file.flush()
        (out_scope, result) = tychon.run_string(trim_margin(f"""
            define(fname '{temp_file.name}')
            lang_load_module(fname)
            """), scope)
        #  print('!!! result=', pformat(result))
        module = result[-1]
        assert module == { 'a': 1, 'b': 2 }
