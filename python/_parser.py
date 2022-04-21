import tatsu
from collections import namedtuple
from pprint import pformat

#  SHOW_PARSER_TRACE = True
SHOW_PARSER_TRACE = False

GRAMMAR = r'''
    @@whitespace :: / /

    start = { @:line }*;

    eol = '\n' | $;

    line = empty_line | solo_expression | horizontal_list ;
        solo_expression = (@:expression eol) ;
        empty_line = empty_line:eol ;
        horizontal_list = first:expression more:{expression}+ eol;


    #
    # expressions with priority. First is lower priority, Last is higher priority.
    #

    expression = bracket_list  | function_call
                 | colon_function_call | indented_list | binary_operation;
        bracket_list = '[' ~ @:{expression}* ']';
        function_call = func:identifier '(' args:{ expression } * ')' ;
        colon_function_call = func:identifier '::' ~ args:(horizontal_list | indented_list) ;
        indented_list = '$$INDENT$$' ~ eol @:{ line }+ '$$OUTDENT$$' ;

    #
    #     binary operations
    #

    binary_operation = addition | subtraction | binary_2 ;
            addition = left:binary_operation op:'+' ~ right:binary_2 ;
            subtraction = left:binary_operation op:'-' ~ right:binary_2 ;

        binary_2 = multiplication | division | binary_1 ;
            multiplication = left:binary_2 op:'*' ~ right:binary_1 ;
            division = left:binary_2 op:'/' ~ right:binary_1 ;

        binary_1 = parentheses | term ;
            parentheses = '(' ~ @:expression ')' ;
    #
    # terms
    #

    #  term = integer;
    term = single_quote_string | double_quote_string | float | integer | identifier ;
        single_quote_string = "'" ~ string:/[^']*/ "'" ;
        double_quote_string = '"' ~ string:/[^"]*/ '"' ;
        float = /\d+\.\d+/ ;
        integer = /[0-9]+/ ;
        identifier = /[a-zA-Z_][a-zA-Z_0-9]*/ ;
'''
PARSER = tatsu.compile(GRAMMAR)

def parse(source):
    '''Parse a string and return the AST'''
    source = _insert_indentation_symbols(source)
    tychon_ast = PARSER.parse(source,
                          parseinfo=True,
                          comments_re=None,
                          semantics=TychonSemantics(),
                          colorize=SHOW_PARSER_TRACE,
                          trace=SHOW_PARSER_TRACE)
    #  print('!!! parse() tychon_ast=', repr(tychon_ast))
    return tychon_ast

def _insert_indentation_symbols(source):
    '''
    Convert indentation into $$INDENT$$ and $$OUTDENT$$ symbols so that our PEG grammar can see it
    '''
    result = []
    last_indent = 0
    for line in source.split('\n'):
        this_indent = len(line) - len(line.lstrip())

        if this_indent > last_indent:
            result[-1] =  result[-1] + ' $$INDENT$$'
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
AAA $$INDENT$$
    BBB
    CCC
    $$OUTDENT$$
DDD'''
    assert _insert_indentation_symbols(source) == expected

class Call:
    def __init__(self, args):
        assert isinstance(args[0], Sym)
        self.function_name = args[0].name
        self.args = args[1:]

    def __repr__(self):
        return "{}({})".format(
            self.function_name,
            " ".join(repr(i) for i in self.args)
        )

    def __eq__(self, other):
        return isinstance(other, Call) and self.function_name == other.function_name and self.args == other.args

class Sym:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Sym) and self.name == other.name

    def __hash__(self):
        return self.name.__hash__()

class TychonSemantics:

    def vertical_list(self, ast, *rule_params, **kwparams):
        return list(ast)

    def horizontal_list(self, ast, *rule_params, **kwparams):
        #  print('!!! horizontal list ast=', repr(ast), 'rule=', repr(rule_params), 'kw=', repr(kwparams))
        the_list = [ast['first']] + ast['more']
        if 'last' in ast: the_list.append(ast['last'])
        return the_list

    def addition(self, ast, *rule_params, **kwparams):
        return Call([Sym('add'), ast['left'], ast['right']])

    def subtraction(self, ast, *rule_params, **kwparams):
        return Call([Sym('subtract'), ast['left'], ast['right']])

    def multiplication(self, ast, *rule_params, **kwparams):
        return Call([Sym('multiply'), ast['left'], ast['right']])

    def division(self, ast, *rule_params, **kwparams):
        return Call([Sym('divide'), ast['left'], ast['right']])

    def function_call(self, ast, *args, **kwargs):
        return Call([Sym(ast['func'].name), *ast['args']])

    def colon_function_call(self, ast, *args, **kwargs):
        #  print('!!! colon_function_call ast=\n', pformat(ast))
        return Call([Sym(ast['func'].name), *ast['args']])

    def single_quote_string(self, ast):
        return ast['string']

    def double_quote_string(self, ast):
        #  print('!!! double_quote_string() ast=', repr(ast))
        return ast['string']

    def integer(self, ast, *rule_params, **kwparams):
        return int(ast)

    def float(self, ast, *rule_params, **kwparams):
        return float(ast)

    def identifier(self, name, *args, **kwargs):
        #  print('!!! identifier() name=', repr(name), 'args=', repr(args), 'kwargs=', repr(kwargs))
        return Sym(name)
