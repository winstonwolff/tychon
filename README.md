Tychon — An embedded language so users can "program" or "script" within your program

Goals:

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
- Syntax error messages from parser
- REPL
- Define functions
- Searching operators, e.g. '(a == 1 or a == 3) and (b == 0)'


Idea
----

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
