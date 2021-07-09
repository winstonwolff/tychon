import io
import tychon

def test_hello_world():
    out = io.StringIO()
    tychon.run("print('hello' 'world')", out)
    assert out.getvalue() == 'hello world\n'




