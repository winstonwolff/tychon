import io
import tychonian

def test_hello_world():
    out = io.StringIO()
    tychonian.run("print('hello' 'world')", out)
    assert out.getvalue() == 'hello world\n'




