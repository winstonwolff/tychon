Want
====
- Types are defined by functions, not by the language's DSL. I.e. a variable is of type T, and there
  is a function that determines of a value complies or not. When a function requires inputs of type
  T, the programmers's function is used.

- A way to describe and enforce "programming in the large":
  - demeter's law
  - related to demeter's law, define zones in your app, and declare which zones can access functions
    from other zones. Implemented as a module's type, the types that a module is allowed to import
  - functions can be declared as "pure" and the compiler checks it.
  - modules can be declared "safe" or "pure" and the compiler checks it.

- compilation should be an optimization — the idea of compiling a program is really just pre-processing.
  C is faster than Python or Ruby, but it loses some expressiveness. Shouldn't the programmer
  determine the efficiency/expressiveness tradeoff they need for the problem at hand?  E.g. If you
  know you are sorting integers, the VM can call the integer sort directly. If you are sorting
  objects of unknown type, the VM must check each object before sorting. Depending on the problem,
  you can do either. In the first case, declare the inputs as always integers, and the VM can
  pre-compute the sorting function to use.


Aesthtics:
  - unify notations for dictionaries, classes, and variables
  - unify notations for lists of data, and lists of statements:
    - e.g. no commas at end of lines,
    - no commas between function arguments

### Idea 5
Back to just describing data — a language can come later.

    # A comment

    # some primative values:
    42 6.28 -1 3e8 3i 1_000_000  # some numbers
    'a string' "another string using double-quotes"  # strings

    'this' 'is' 'a' 'list' 'on' 'one' 'line'

    'one'
    'list'
    'on'
    'several'
    'lines'

    # 3x3 matrix, i.e. nested array
    1 0 0
    0 1 0
    0 0 1

    'this' 'is'
        \ 'one' 'list'
        \ 'on' 'several' 'lines'

    'a' 'list' ['sub' 'list']  # this is a three element list

    # Equivalent to previous
    'a' 'list':
        'sub' 'list'

    # Equivalent to previous
    'a' 'list':
        'sub'
        'list'

    #
    # Adding symbols and operators
    #

    a_symbol

    # labeling operator
    a: 'this string is labeled "a"'

    # Dictionary
    a: 'one' b: 'two' c: 'three'
    a: 'one'
    b: 'two'
    c: 'three'

    # function call with indexed and named arguments
    a := print('!!! stuff=' a b c end: '\r')

    # operator precedence
    . (method_lookup)
    : (label operator)
    * / // (floor division) % (modulus) @ (matrix dot product)
    + -
    > < >= <= <> (not equal) != (also not equal)

    a : my_instance . my_method
    a : method_lookup(my_instance my_method)

    #
    # Put it together
    #

    def print(*args sep:' ' end:'\n'):
        foo
        bar
        baz


## Idea 0

primative types:
    Int  5_500
    Float 31.4e-1
    String 'blah'  """multi line string"""
    List   [1, 2, 3]
    Dictionary {'a': 1, 'b': 2}
    Set {1, 2, 3}
    ArgList = ([args] {kwargs})
    Symbol = name of something in the Scope
    Scope
    Function
    Type

primitive operations:
    name things = add name in Scope, pointing to something
    lookup symbol in Scope
        - <name symbol>
        - x.y
        - @x
    call a function f(x)  x >> f  x | f
    grouping:
        - with parens: ( <some stuff> )
        - with separators:  a b c, d e f  == (a b c) (d e f)
        - newlines are separators too
    annotate:
        - doc strings
        - types

    parse(text) -> ast_tree
    compile(ast_tree) -> ast_tree
      is compile() the same as optimize()? I.e. you are pre-fetching constants, symbol lookups, etc?
    run -> runs in VM

collections
    List
    Dictionary

parsing sugar
    infix operators for functions
    pipe operator for function calls

Here we define some functions:
    add : (x, y) -> x + y
    multiply : (a, b) -> a * b

some constants:
    J:  3
    anotherConst: "blah"

some variables:
    a_list: [1, 2, 3]
    list_2:
        1
        2
        3
    dict_a: {'a': 3, 'b': 4}
    dict_b: Dict(:)
        'a': 3
        'b': 4

myfunc: (a) ->
    b: add(a, a)
    c: multiply(b, b)

MyClass: class(
    constructor: (@props)
        @state = {
            'sum': @a + @b
    render:


## Idea 1

    Calling functions:
        ? add 1 2                           -- add(1, 2)
        ? def double (a b) (multiply 2 a)   -- def double(a): return 2 * a

    Defining data:
        mynumber := 3.14
        define $ mynumber 3.14
        mylist := [1 2 3]
        mylist := [:
            1
            2
            3
        mydict := { a: b c: d e: f}
        mydict :=
            a: b
            c: d
            e: f

    ## Assignment is a function
      a := 1
    same as:
      scope.define('a' 1)

    ## defining a function

## Idea 2
    Since code is just data that is executed, we don't need to focus on programming, just data.

    Function Call:
        CALL multiply 3 4

    Arrays
        Arrays can be created by calling the Array constructor
            CALL Array 1 2 3 'a' 'b' 'c'
        Shortcut is surround by brackets
            [ 1 2 3 'a' 'b' 'c' ]
        Can also be created by calling constructor with colon ":" with elements on separate lines
            call Array:
                'a'
                'b'
                'c'

    Scopes are Dictionaries. You define them similarly.
        Dictionaries:
            CALL Dictionary [ one: 1 two: 2 three: 3 ]
            o = 'one'
            [ o 1 two: 2 ]

        Scopes:
            Global
            Module (source file)
            Function
            Block
            Class
            Instance

            DEFINE <scope> <name> <value>
            DEFINE global x 3
            global['x'] = 3

    Function Definition — Blocks of code are Arrays of expressions
        DEFINE <name> function <args = array of symbols> <array of expressions>
        DEFINE multiply function [a b] [(CALL multiply a b)]
        multiply: (a b) ->
            CALL multiply a b

    def abc(a, b, c):
        return a * b

    (foo (a b)(base: 3 bar: 4))
    (foo a b base:3 bar:4)

### Idea 3
Can we make a unified syntax where many things are function calls, but with
different orders?

    class – is a function that takes a list of functions as methods.
        class Dict:
            function set(self, key, value):
                ...

            function get(self, key):
                ...
        equivalent to:
            class( 'Dict', [
                function('set', ['key', 'value'], ...),
                function('get', ['key'], ...)
            ])

    decorators -- a function that operates on the expression that follows

        class Foo:
            static function bar():...
            # static() is a function that modifies bar()'s definition

        equivalent to:
            class( 'Foo', [
                static(
                    function('bar', [], ...)
                ) ]
            )


    chains of methods

        myDict
        | filter(...)
        | map(...)

        eqivalent to: map( filter( myDict, ...), ...)

    tree structures

        html()
            .div(class="content")
                .p
                    .text("Here is some content")
        equivalent to:

            div("#my_id.content")(
                p()("Here is some content")
            )
### Idea 4
    function double(x):
        x * x

    macro class(name definition):
        ...

    macro type(name definition):
        ...

    macro if [predicate true_expression false_expression]


