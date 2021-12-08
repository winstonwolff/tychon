import tatsu
from collections import namedtuple

#  SHOW_PARSER_TRACE = True
SHOW_PARSER_TRACE = False

GRAMMAR = r'''
    @@whitespace :: / +/

    start = { line | vertical_list | empty_line }*;

    vertical_list = '$$INDENT$$' ~ EOL vertical_list:{ line }+ '$$OUTDENT$$' EOL;

    line = (@:expression EOL) | ( @:{ expression }+ EOL );

    empty_line = empty_line:'\n';

    #
    # expressions with priority. First is lower priority, Last is higher priority.
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
        | bracket_list
        ;

    bracket_list =
        | '[' ~ @:{ expression }+ ']'
        | expr0
        ;

    #  expr0 = | function_definition | function_call | term ;
        #  function_definition = 'func' name:identifier '(' args:{ identifier }* '):' body:expression;
        #  function_call = func:identifier '(' args:{ expression } * ')' ;
    expr0 = | function_call | term ;
        function_call = func:identifier '(' args:{ expression } * ')' ;

    #
    # terms
    #

    term = string | number | identifier ;

        string = single_quote_string | double_quote_string ;
            single_quote_string = "'" ~ string:/[^']*/ "'" ;
            double_quote_string = '"' ~ string:/[^"]*/ '"' ;

        number = float | integer ;
            float = /\d+\.\d+/ ;
            integer = /[0-9]+/ ;

        identifier = /[a-zA-Z_][a-zA-Z_0-9]*/ ;

    EOL = '\n' | $;
'''
PARSER = tatsu.compile(GRAMMAR)

def parse(source):
    '''Parse a string and return the AST'''
    source = _insert_indentation_symbols(source)
    parsed = PARSER.parse(source,
                          parseinfo=True,
                          comments_re=None,
                          semantics=TychonSemantics(),
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

#  Call = namedtuple('Call', ['args'])

class Call(tuple):
    def __new__(self, *args):
        return tuple.__new__(Call, *args)

    def __repr__(self):
        return "Call({})".format(", ".join(repr(i) for i in self))

    #  def __eq__(self, other):
    #      return isinstance(other, Call) and tuple(self) == tuple(other)

class Sym:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Sym('{}')".format(self.name)

    def __eq__(self, other):
        return isinstance(other, Sym) and self.name == other.name

    def __hash__(self):
        return self.name.__hash__()

class TychonSemantics:

    def addition(self, ast, *rule_params, **kwparams):
        return Call([Sym('add'), ast['left'], ast['right']])

    def subtraction(self, ast, *rule_params, **kwparams):
        return Call([Sym('subtract'), ast['left'], ast['right']])

    def multiplication(self, ast, *rule_params, **kwparams):
        return Call([Sym('multiply'), ast['left'], ast['right']])

    def division(self, ast, *rule_params, **kwparams):
        return Call([Sym('divide'), ast['left'], ast['right']])

    def function_call(self, ast, *args, **kwargs):
        print('!!! function_call() ast=', repr(ast), 'args=', repr(args), 'kwargs=', repr(kwargs))
        return Call([Sym(ast['func'].name), *ast['args']])

    def function_definition(self, ast, *args, **kwargs):
        print('!!! function_definition() ast=', repr(ast), 'args=', repr(args), 'kwargs=', repr(kwargs))
        return Call([Sym('function'),
                     Sym(ast['func'].name),
                     ast['args'],
                     ast['code'],
                    ])

    def single_quote_string(self, ast):
        return ast['string']

    def double_quote_string(self, ast):
        return ast['string']

    def integer(self, ast, *rule_params, **kwparams):
        return int(ast)

    def float(self, ast, *rule_params, **kwparams):
        return float(ast)

    def identifier(self, name, *args, **kwargs):
        #  print('!!! identifier() name=', repr(name), 'args=', repr(args), 'kwargs=', repr(kwargs))
        return Sym(name)
