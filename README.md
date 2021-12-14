Tychon — An embedded language so users can "program" or "script" within your program

Goals:

    Familiar
        - a language that feels like Ruby or Python

    Driving Feature? Who would adopt it?
        - embeddable in other people's programs as text editor or graphical block language
            WHO: Zapier, Slack Workflows, Logic AND OR statements
        - compiles to WebASM. Run it on CloudFlare.
            WHO: Cloudflare
        - as Python scripts your computer, Tychon scripts the internet. With one line, call APIs in
          REST, Graph QL, and some pre-made api bindings, e.g. Github, Gmail, Slack
          - distributed computing
            WHO: general populace

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

    Programming in the Large
        - has Macros to expand the language (like Lisp/Clojure)
            - AST looks like Clojure, i.e. `1 + 1` == `add(1 1)` == Call(add 1 1)
        - Macro/function for marking functions pure, and checking that it's so
        - Macro/function for enforcing Law of Demeter
        - Macro/function for enforcing knowledge of other modules, e.g. Controllers know all, but Models cannot know Views, and Views cannot know Controllers
        - macros must be in marked modules, so people don't use them too much



Usage
-----
  ./run.sh
  ./tychon.py <sourcefile>.ty

TODO
----
- REPL
- Syntax error messages from parser

DONE
----
- Define functions

Ideas
-----

Unify lines of code with Dictionary definitions
  : — assignment
  = — define a constant

Function definitions are macros
  add = func(a b): a + b
  add = func(a:Integer b:Integer): a + b                # with type annotation
  add = func(a=1 b=2): a + b                            # with default values
  add = func(a:Integer=1 "the first operand"            # arguments with docstrings
             b:Integer=2 "the second operand"):
             "returns the sum of of 'a' and 'b'"
             a + b
  double = lambda(_ * 2)

Dictionaries:
    dict = Dict(a:1 inc:(func(self):self.a + 1))
    list = [1 2 4]
    list =
        1
        2
        4


Chained calling

    list
        |> map( _ * 2)
        |> filter( isEven(_) )

    equivalent to:
        a = map(list, _ * 2)
        b = filter(a, isEvent(_) )

Prefix calling

    static <| pure <| Class User:
        name:String=""
        email:String="unknown@example.com"


All notations have horizontal and vertical notation
    list:
        [a b c]                         # one-liner
        a                               # vertical
        b
        c

    create a dictionary:
        dictionary(a:1 b:2)
        @dictionary
            a:1
            b:2

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
        f( g( n ))

        @f
        @g
        n

    named function arguments
        print(1 3 end:'\n' sep:' ')

    define a constant:
        constant(pi 3.14)               # f() notation
        pi := 3.14                      # infix notation
        @constant
            pi 3.14
            tau 6.28

    anonymous function
        function(a [a * 2])             # f() notation
        a -> a * 2                      # infix notation
        a ->                            # vertical
            a * 2

        a                               # more vertical
        ->
        a * 2

    function definition:
        constant(sum function([a b] [[a + b]]))   # f() notation one-liner

        @constant                       # f() notation vertical
            sum
            @function
                a b
                a + b

        sum := (a b) -> a + b     # infix one-liner

        sum :=                          # infix vertical
            a
            b
        ->
            a + b


    function arguments can take default values, doc strings, and other annotations
        sum: function( [[a doc:'first argument'] [b:3 doc:'second argument']] [a + b])
        sum: (a b) -> a + b
        sum:                          # vertical
            a
            b:3 type:Integer doc:'the second value'
        ->
            a + b

    labels:
        a:1
        label('a' 1)
        label('my_dict' dictionary(label('a' 1) label('b' 2)))

Unify notation for dictionaries, argument lists, function bodies
    dictionary(a:1 b:2)
    print(1 2 sep:' | ')
    (a b) ->
        a_squared: a ** 2                       # define constants
        b_squared: b ** 2
        two_a_b: 2 * a * b
        a_squared + b_squared + two_a_b         # return last value

    Dictionaries evaluate labels to create data structure
        dictionary( label('a' 1) label('b' 2))

    Argument lists interpret labels to fill out the argument list

    Function bodies evaluate labels as constant definitions


variables are separate from constants
    pi: 3.14            # a constant named 'pi'
    a = 1               # a variable named 'a'
    a = pi * a          # change variable 'a'
    a += 1              # increment a

    pi: 3.14

