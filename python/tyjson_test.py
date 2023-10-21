import pytest
import tyjson

from _parser import Sym, Call

def test_dump_string():
    assert tyjson.dump("a string") == '"a string"'

def test_dump_integer():
    assert tyjson.dump(345) == '345'

def test_dump_float():
    assert tyjson.dump(345.67) == '345.67'

def test_dump_Sym():
    assert tyjson.dump(Sym('my_symbol')) == '["Symbol", "my_symbol"]'

def test_dump_Call():
    parseinfo = {}
    assert tyjson.dump(Call([Sym('my_function'), 1, "a string", Sym("my_symbol")])) == '["my_function", 1, "a string", ["Symbol", "my_symbol"]]'


