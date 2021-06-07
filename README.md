Goal: Make a simple parser for building data structures. I could be used for
      HTML, Specs, GUI definitions.

Usage
-----
  ./main.py
  pytest -v main.py — run tests

TODO
----
- Make an output from parser, e.g.
  `foo 1 2 3` -> [ <foo>, 1, 2, 3 ]
- combine with yaml_lang


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
