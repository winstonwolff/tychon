TODO
----
* minimal language: functions, macros, arithmetic

    - DONE evaluating a variable fetches it's value
    - DONE if(predicate true_block else: false_block)
    - DONE Fix grammar so single elements on a line evaluate to just that element, not a list of one element
    - DONE Failing test: foo(1 2) = (3,)
    - DONE user can define macros

Next:
    - functions or macros with multi-line blocks

    - user-defined functions (or macros) can manipulate Scope
    - Tychon program to generate documentation, i.e. doctest
        - can load a file as AST graph, and evaluate later
    - make 'func' a macro which evaluates it's args first

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
    - := — set variable
    - = — define constant

* Apply Tychon to something
    - DSL or Macros for asserting the shape of data (related to typing)
    - Replacement for SASS, that can also write unit tests for CSS.
    - DSL or Macros for automated testing
    - DSL or Macros for generating html

* WASM engine
    - execute browser via WASM

DONE
----
- REPL
- Define functions



Ideas
-----

    named function arguments
        print(1 3 end='\n' sep=' ')

    define a constant:
        constant(pi 3.14)               # f() notation
        pi = 3.14                      # infix notation
        @constant
            pi 3.14
            tau 6.28

    define a variable, i.e. mutable reference
        variable(a 55)
        a := 55

    define function
        func(double [a] [a * 2])
        double(3)               # -> 6

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
