Tychon — An embedded language so users can "program" or "script" within your program

Usage
-----
  ./run_tests.sh
  ./tychon.py <sourcefile>.ty

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

Goals:
------

    Driving Feature? Who would adopt it?
        - compiles to WebASM. Run it on CloudFlare.
            WHO: Cloudflare
        - embeddable in other people's programs as text editor or graphical block language
            WHO: Zapier, Slack Workflows, Logic AND OR statements, Gitlab or CirceCI yaml, AirTable

    Familiar
        - a language that feels like Ruby or Python

    Beautiful
        Visually
        - significant indentation for blocks
        - but even less syntax: no commas
        - notation for tree structures
        Conceptually
        - Unify concept of writing: (a) lines of a function, (2) dictionaries, and (3) calling parameters
        - Macro/function for docstrings

    Functional
        - mostly immutable data structures like Clojure
        - "functions" are pure, and are clearly marked
        - procedures are like functions but may have side-effects. Unlike Pascal, procedures may
          return values

    Compilation is just a form of Optimization
        - Macro for enforcing constraints, e.g. on inputs and outputs, which can be used by
          optimizer
        - Instead of a compiler, have an optimizer that searches for things that can be
          pre-computed or unrolled for speed.
        - repetitions can be combined to save memory
        - Can indicate if you want to optimize for speed or memory.

    Types are programmable
        - Since there is no compilation phase, just an optimization phase, types
          can be programmed like normal code.
        - Type checking means calling a function to see if this is in fact a type.
        - Some optimizations can use type assertions to simplify code or reduce
          memory footprint.

    Programming in the Large
        - has Macros to expand the language (like Lisp/Clojure)
            - AST looks like Clojure, i.e. `1 + 1` == `add(1 1)` == Call(add 1 1)
        - Macro/function for marking functions pure, and checking that it's so
        - Macro/function for enforcing Law of Demeter
        - Macro/function for enforcing knowledge of other modules, e.g. Controllers know all, but Models cannot know Views, and Views cannot know Controllers
        - macros must be in marked modules, so people don't use them too much



Ideas
-----


Calling functions
    Mathematical notation
        sum(1 2)        # returns 3

    Chained calling

        list
            |> map( _ * 2)
            |> filter( isEven(_) )

        equivalent to:
            a = map(list, _ * 2)
            b = filter(a, isEvent(_) )

    Prefix calling

        static:
        pure:
        class User:
            name: "" type: String doc: "Moniker of person"
            email: "unknown@example.com" type: String doc: "how to contact them"

        @class User
            name
            email
            greeting: \ 'hello {}'.format(name)


All notations have horizontal and vertical notation
    list:
        [a b c]                         # one-liner
        a                               # vertical
        b
        c

    strings:
        "i am a string"
        'single quote string'
        """
        multi
        line
        string
        """

    comments:
        # one line comment
        ###
        multi
        line
        comment
        ###

    function call:
        f(a b c)                        # one-liner using f() notation
        @f                              # vertical notation without parentheses
            a
            b
            c

        f( g( n ))                      # function call, regular math notation

        f(): g(): n                       # ??? function call that is more convenient with indention
        f():
            g():
                n

        n |> g |> f                     # reverse function call

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

    anonymous function
        func(a [a * 2])                 # f() notation
        (a) -> a * 2                    # infix notation
        (a) ->                          # vertical
            a * 2

        a                               # more vertical
        ->
        a * 2

    writing modes
        - Tychon code
        - HTML a la JSX
        - Human text, i.e. documentation
        - executable examples within documentation


### Automated Testing

func(:) add [a b]:
    '''
    Returns the sum of `a` and `b`.

    >>> add(1 2)
    3

    >>> add(0 0)
    0
    '''
    a + b

describe 'add()':
    test 'returns the sum of arguments':
        expect(add(3 4)).to eq(7)


### HTML generation, a la JSX

import(render html body h1 div ul li from: TSX)

func<:> MyComponent [explative product_name]
    div(:)id='MyComponent' class=['first' 'second']
        h1(:)class='foo' id='blah'
            "This is my string"
        p(:) class="plain_paragraph"
            Ut dolor aliqua dolor dolor culpa aliqua minim non enim aliquip cillum veniam id.  Do ut
            in cillum laborum ut voluptate.  Sit duis in adipiscing lorem est in ad consequat
            aliquip laboris.

func<:> MyPage [goods_for_sale]
    div(:) id="MyPage"
        goods_for_sale |> map(-> MyComponent('Buy now for a limited time only' %1))

@main
func<:> [stdin stdout]
    skews = ['12113' '3342']
    render(MyPage)
