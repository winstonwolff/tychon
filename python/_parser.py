import tatsu
from collections import namedtuple
from pprint import pformat
from _util import trim_margin

#  SHOW_PARSER_TRACE = True
SHOW_PARSER_TRACE = False

GRAMMAR = r'''
    @@whitespace :: / ,/

    start = { @:line }*;

    eol = '\n' | $;

    line = empty_line | horizontal_list ;
        empty_line = empty_line:eol ;
        horizontal_list = (@:{ expression }+ eol) ;


    #
    # expressions with priority. First is lower priority, Last is higher priority.
    #

    expression = bracket_list  | function_call | colon_function_call
            | indented_list | binary_operation;
        bracket_list = '[' ~ @:{expression}* ']';
        function_call = func:identifier '(' args:{expression}* ')' ;
        colon_function_call = func:identifier '::' ~ args: (indented_list | {expression}+);
        indented_list = '$$INDENT$$' ~ eol @:{ line }+ '$$OUTDENT$$' ;

    #
    #     binary operations
    #

    binary_operation = addition | subtraction | binary_3 ;
            addition = left:binary_operation op:'+' ~ right:binary_3 ;
            subtraction = left:binary_operation op:'-' ~ right:binary_3 ;

        binary_3 = multiplication | division | binary_1 ;
            multiplication = left:binary_3 op:'*' ~ right:binary_1 ;
            division = left:binary_3 op:'/' ~ right:binary_1 ;

        #  binary_2 = equal | not_equal : binary_1;
        #      equal = left:binary_2 op:'==' ~ right:binary_1;
        #      not_equal = left:binary_2 op:'!=' ~ right:binary_1;

        binary_1 = parentheses | term ;
            parentheses = '(' ~ @:expression ')' ;
    #
    # terms
    #

    term = single_quote_string | double_quote_string | float | integer | identifier ;
        single_quote_string = "'" ~ string:/[^']*/ "'" ;
        double_quote_string = '"' ~ string:/[^"]*/ '"' ;
        float = /\d+\.\d+/ ;
        integer = /[0-9]+/ ;
        identifier = value:/[a-zA-Z_][a-zA-Z_0-9]*/ ;
'''
PARSER = tatsu.compile(GRAMMAR)

def parse(source, source_fname=None):
    '''Parse a string and return the AST'''
    source = _insert_indentation_symbols(source)
    #  print('!!! parse() source===\n', source, '\n===')
    tychon_ast = PARSER.parse(source,
                          filename=source_fname,
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
    INDENT_SIZE = 4
    result = []
    last_indent = 0
    for line_no, line in enumerate(source.split('\n')):

        unindented_line = line.lstrip()
        unindented_len = len(unindented_line)
        if unindented_len > 0:
            indent_spaces = len(line) - unindented_len
            if indent_spaces % INDENT_SIZE != 0:
                raise IndentationError('Indentation should be 4 spaces {} line: {}'.format(line_no, line))
            this_indent = int(indent_spaces / INDENT_SIZE)

            if this_indent > last_indent:
                result[-1] = result[-1] + ' $$INDENT$$'
            elif this_indent < last_indent:
                for i in range(last_indent, this_indent, -1):
                    result.append((' ' * i * INDENT_SIZE) + '$$OUTDENT$$')
            last_indent = this_indent

        result.append(line)

    for i in range(last_indent, 0, -1):
        result.append((' ' * i * INDENT_SIZE) + '$$OUTDENT$$')


    return '\n'.join(result)

def test_insert_indentation_symbols():
    source = trim_margin('''
        AAA
            BBB
            CCC
        DDD
        ''')
    expected = trim_margin('''
        AAA $$INDENT$$
            BBB
            CCC
            $$OUTDENT$$
        DDD
        ''')
    assert _insert_indentation_symbols(source) == expected

def test_double_indentation_symbols():
    source = trim_margin('''
        AAA
            BBB
                CCC
        DDD
        ''')
    expected = trim_margin('''
        AAA $$INDENT$$
            BBB $$INDENT$$
                CCC
                $$OUTDENT$$
            $$OUTDENT$$
        DDD
        ''')
    assert _insert_indentation_symbols(source) == expected

def test_indentation_with_emtpy_lines():
    source = trim_margin('''
        AAA
            BBB

                CCC
        DDD
        ''')
    expected = trim_margin('''
        AAA $$INDENT$$
            BBB
         $$INDENT$$
                CCC
                $$OUTDENT$$
            $$OUTDENT$$
        DDD
        ''')
    assert _insert_indentation_symbols(source) == expected

def test_indentation_with_no_last_line():
    source = trim_margin('''
        AAA
            BBB
                CCC
        ''').strip()
    expected = trim_margin('''
        AAA $$INDENT$$
            BBB $$INDENT$$
                CCC
                $$OUTDENT$$
            $$OUTDENT$$
        ''').strip()
    assert _insert_indentation_symbols(source) == expected

class AstNode:
    def __init__(self, parseinfo):
        self.parseinfo = parseinfo

class Call(AstNode):
    def __init__(self, args, parseinfo=None):
        super().__init__(parseinfo)
        assert isinstance(args[0], Sym)
        self.function_name = args[0].name
        self.args = args[1:]

    def __repr__(self):
        return "{}({})".format(
            self.function_name,
            " ".join(repr(i) for i in self.args)
        )

    def __eq__(self, other):
        return isinstance(other, Call) \
                and self.function_name == other.function_name \
                and self.args == other.args

class Sym(AstNode):
    def __init__(self, name, parseinfo=None):
        super().__init__(parseinfo)
        self.name = name

    def __repr__(self):
        return f'`{self.name}`'

    def __eq__(self, other):
        return isinstance(other, Sym) and self.name == other.name

    def __hash__(self):
        return self.name.__hash__()


class TychonSemantics:

    def empty_line(self, ast, *rule_params, **kwparams):
        return None

    def indented_list(self, ast, *rule_params, **kwparams):
        return list(ast)

    def horizontal_list(self, ast, *rule_params, **kwparams):
        if len(ast) == 1:
            result = ast[0]
        else:
            result = list(ast)
        return result

    def addition(self, ast, *rule_params, **kwparams):
        return Call([Sym('add', ast['parseinfo']), ast['left'], ast['right']], ast['parseinfo'])

    def subtraction(self, ast, *rule_params, **kwparams):
        return Call([Sym('subtract', ast['parseinfo']), ast['left'], ast['right']], ast['parseinfo'])

    def multiplication(self, ast, *rule_params, **kwparams):
        return Call([Sym('multiply', ast['parseinfo']), ast['left'], ast['right']], ast['parseinfo'])

    def division(self, ast, *rule_params, **kwparams):
        return Call([Sym('divide', ast['parseinfo']), ast['left'], ast['right']], ast['parseinfo'])

    def equality(self, ast, *rule_params, **kwparams):
        return Call([Sym('equal', ast['parseinfo']), ast['left'], ast['right']], ast['parseinfo'])

    def not_equal(self, ast, *rule_params, **kwparams):
        return Call([Sym('not', ast['parseinfo']),
                     Call([Sym('equal', ast['parseinfo']), ast['left'], ast['right']], ast['parseinfo'])
                    ], ast['parseinfo'])

    def function_call(self, ast, *args, **kwargs):
        #  print('!!! function_call ast=\n', pformat(ast))
        return Call([Sym(ast['func'].name, ast['parseinfo']), *ast['args']], ast['parseinfo'])

    def colon_function_call(self, ast, *args, **kwargs):
        #  print('!!! colon_function_call ast=\n', pformat(ast))
        return Call([Sym(ast['func'].name, ast['parseinfo']), *ast['args']], ast['parseinfo'])

    def single_quote_string(self, ast):
        return ast['string']

    def double_quote_string(self, ast):
        #  print('!!! double_quote_string() ast=', repr(ast))
        return ast['string']

    def integer(self, ast, *rule_params, **kwparams):
        return int(ast)

    def float(self, ast, *rule_params, **kwparams):
        return float(ast)

    def identifier(self, ast, *args, **kwargs):
        #  print('!!! identifier() name=', repr(name), 'args=', repr(args), 'kwargs=', repr(kwargs))
        return Sym(ast['value'], ast['parseinfo'])
