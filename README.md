# Tychon — An experiment in a python-y smalltalk-y lisp-y embedded language.

Usage
-----
  ./run_tests.sh                        # run the tests
  ./tychon.py <sourcefile>.ty           # execute a source file
  ./tychon.py                           # a REPL

Examples
--------

Math is familiar:
```
>>> 2 + 4
6
```

Function calls are also similar, although note that there are no commas separating arguments
```
>>> print('two times four is' 2 * 4)
two times four is 8
```

Defining a function looks like a function itself, although it's actually a macro.
```
>>> func(double [a] [a * 2])
>>> double(3)
6
```

Functions evaulate their arguments before being called. Macros take all arguments as-is,
without evaluating. So you can evaluate them later, or manipulate them:
```
>>> macro(debug_print [sym] [print('log:' sym '=' evaluate(sym))])
>>> a = 1
>>> debug_print(a)
log: a = 1
```



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
        - macros definitions must be in marked modules, so people don't use them too much


