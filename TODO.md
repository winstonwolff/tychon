Thoughts on Tychon values and metadata for them

value
    - name
    - exported
    - doc string

TODO
====
    - Tychon program to generate documentation, i.e. doctest
        - DONE generate_docs.ty -> docs.html
        - DONE --verbose flag
        - group functions together in the documentation


    - import()
        DONE - read_code() which reads file and returns structure of the code, e.g. lists of values
          and function calls
        - load_module() which reads module, then executes it, returning the results of those
          calls, e.g. a bunch of functions, constants, variables
        - export() which accumulates values, or marks the values somehow
        - import which loads module and adds values to current scope

    - write_code() — opposite of prelude.read_code()

    - We have _buitins.func() which evaluates its arguments, but
      _evaluator.evaluate() also does that. Do we need both?

    - _builtins.func() defines an inner class. Can that be an outer class instead?



* Graphical multi-user-dungeon
    - Rooms with an image
    - hot spots which activate a script when clicked
    - script can print a message, or go to another room

    - constant(name value scope:@scope)
    - variable(name value scope:@scope)
    - range()
    - map()
    - for()
    - Syntax error messages from parser

* Nicer Syntax:
    - a := 1            # set a variable e.g. variable('a' 1)
    - PI = 3.14         # define constant, e.g. constant('PI' 3.14)
    - { a:1 b:2 } — dictionary
      dictionary( label('a' 1) label('b' 2) )
    - argument lists
        - print('a' sep:'_') — Call with default arguments
          print('a' label('sep' '_'))
        - args=['a' sep:'_']
          print(*args)       — splat arguments

* Apply Tychon to something
    - DSL or Macros for automated testing
    - DSL or Macros for asserting the shape of data (related to typing)
    - Replacement for SASS, that can also write unit tests for CSS.
    - DSL or Macros for generating html

* WASM engine
    - execute browser via WASM


Ideas
-----

    named function arguments
        print(1 3 end='\n' sep=' ')

    define a constant:
        constant(pi 3.14)               # f() notation
        pi = 3.14                       # infix notation
        @constant
            pi 3.14
            tau 6.28

    define a variable, i.e. mutable reference
        variable(a 55)
        a := 55

    define function
        func(double [a] [a * 2])
        double(3)                       # -> 6

    anonymous function
        func([a] [a * 2])
        func :: [a]
            a * 2
        lambda( _ * 3)

    writing modes
        - Tychon code
        - HTML a la JSX
        - Human text, i.e. documentation
        - executable examples within documentation


### Automated Testing

func::add [a b]
    '''
    Returns the sum of `a` and `b`.

    >>> add(1 2)
    3

    >>> add(0 0)
    0
    '''
    a + b

import :: describe test from: tspec
describe 'add()':
    test 'returns the sum of arguments':
        expect(add(3 4)).to eq(7)


### HTML generation, a la JSX

import(render html body h1 div ul li from: tyhtml)

func:: MyComponent [explative product_name]
    div:: id:'MyComponent' class:['first' 'second']
        h1:: class:'foo' id:'blah'
            "This is my string"
        p:: class:"plain_paragraph"
            '''Ut dolor aliqua dolor dolor culpa aliqua minim non enim aliquip cillum veniam
            id.  Do ut in cillum laborum ut voluptate.  Sit duis in adipiscing lorem est in ad
            consequat aliquip laboris.'''

func:: MyPage [goods_for_sale]
    div:: id:"MyPage"
        goods_for_sale |> map(-> MyComponent('Buy now for a limited time only' %1))

main :: func :: [stdin stdout]
    skews = ['12113' '3342']
    render(MyPage)

### Abstractions

labeled-things (Label? nomination? reference? tagged?)
    Can we abstract and generalize these things?
    - A type which contains a 'name' and a 'value'
        - key-values when creating a dictionary
        - function arguments a la Python can be sequential, or labeled?

        - name:value pair when defining a constant or a variable
        - exporting a symbol from your module takes a label:value pair? -- maybe define() returns a
          nomination that can be exported.

    - Things that have names
        - named functions

    a labeled thing:
    - responds to __label__ and __value__

    type:: Label
        name: String
        value: Any

    type:: Function
        name: String
        doc: String
        parameters: [name, doc, type, default]

