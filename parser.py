import tatsu

#  SHOW_PARSER_TRACE = True
SHOW_PARSER_TRACE = False

GRAMMAR = r'''
    @@whitespace :: / +/

    start = { line | vertical_list | empty_line }*;

    vertical_list = '$$INDENT$$' ~ EOL vertical_list:{ line }+ '$$OUTDENT$$' EOL;

    line = (line:expression EOL) | ( line:{ expression }+ EOL );

    empty_line = empty_line:'\n';

    #
    # expressions with priority
    #

    expression = expr3;

    expr3 = | addition | subtraction | expr2 ;
    addition = left:expr3 op:'+' ~ right:expr2 ;
    subtraction = left:expr3 op:'-' ~ right:expr2 ;

    expr2 = | multiplication | division | expr1 ;
    multiplication = left:expr2 op:'*' ~ right:expr1 ;
    division = left:expr2 op:'/' ~ right:expr1 ;

    expr1 =
        | '(' ~ @:expression ')'
        | function_call
        ;

    function_call =
        | function_call:/[a-zA-Z_][a-zA-Z_0-9]*\(/ args:{ expression } * ')'
        | term
        ;

    #
    # terms
    #

    term = string | number | identifier ;
    string = '"' ~ string:/[^"]*/ '"' ;
    identifier = identifier:/[a-zA-Z_][a-zA-Z_0-9]*/ ;

    number = float | integer ;
    integer = integer:/\d+/ ;
    float = float:/\d+\.\d+/ ;

    EOL = '\n' | $;
'''
PARSER = tatsu.compile(GRAMMAR)

def parse(source):
    '''Parse a string and return the AST'''
    source = _insert_indentation_symbols(source)
    parsed = PARSER.parse(source,
                          parseinfo=True,
                          comments_re=None,
                          colorize=SHOW_PARSER_TRACE,
                          trace=SHOW_PARSER_TRACE)
    return parsed

def _insert_indentation_symbols(source):
    '''
    Convert indentation into $$INDENT$$ and $$OUTDENT$$ symbols so that our PEG grammar can see it
    '''
    result = []
    last_indent = 0
    for line in source.split('\n'):
        this_indent = len(line) - len(line.lstrip())

        if this_indent > last_indent:
            result.append((' ' * this_indent) + '$$INDENT$$')
        elif this_indent < last_indent:
            result.append((' ' * last_indent) + '$$OUTDENT$$')

        result.append(line)

        last_indent = this_indent

    return '\n'.join(result)

def test_insert_indentation_symbols():
    source = '''
AAA
    BBB
    CCC
DDD'''
    expected = '''
AAA
    $$INDENT$$
    BBB
    CCC
    $$OUTDENT$$
DDD'''
    assert _insert_indentation_symbols(source) == expected

