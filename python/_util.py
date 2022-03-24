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

