# Tychon — An experiment in a python-y smalltalk-y lisp-y embedded language.

Usage
-----
  ./run_tests.sh                        # run the tests
  ./tychon.py <sourcefile>.ty           # execute a source file
  ./tychon.py                           # a REPL


Goals:
------

    - Programming language for teams
        - communication
            - reference docs
            - tutorial docs
            - examples
            - executable specifications
        - overview of system — tools to build SVG illustrations of how subsystems relate, with
          hyperlinks into the generated documentation so new developer can get overview of system
          without reviewing every file.
        - relationships - what files are imported by other files? What functions are used by other
          functions?
        - architectural rules — set contraints for how the subsystems may communicate.
            - separation of concerns - E.g.  controllers and views can call models, but not vice versa
            - mark functions as 'pure', and they can only call other 'pure' functions.
            - Eifel style contracts

    -----

    - ** Fix JS warts
        - Cannot use [] notation with my own collection classes
        - . and [] mix the idea of methods and keys
        - I'd like to write JSX-like code without needing a special JSX compiler

    - **Scaffolds beginner programmers** to building reliable systems / programming in the large

    Programming in the Large
        - has Macros to expand the language (like Lisp/Clojure)
            - AST looks like Clojure, i.e. `1 + 1` == `add(1 1)` == Call(__scope__('add') 1 1)
        - Macro/function for marking functions pure, and checking that it's so
        - Macro/function for enforcing Law of Demeter
        - Macro/function for enforcing knowledge of other modules, e.g. Controllers know all, but Models cannot know Views, and Views cannot know Controllers
        - macros definitions must be in marked modules, so people don't use them too much

    Familiar
        - a language that feels like Ruby or Python

    Embeddable in other programs easily
        - block editor that can be external, or embedded in user's program
        - small and simple run-time to execute code

        - automated testing

        - programming by contract -- programmable types


    - multi-threading & messaging to take advantage of cores and immutable data

    - Notation for tree structures
        Since a line of source describes a list of symbols, a tree structure is very
        natural to express. E.g.

            a b c
                d
                e f
        is the same as:
            [a b c [
                d
                [e f]
            ]

    Beautiful
        Visually
        - significant indentation for blocks
        - but even less syntax: no commas
        - notation for tree structures
        Conceptually
        - Unify concept of writing: (a) lines of a function, (b) dictionaries, and (c) calling parameters
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


References on PEG & Packrat parsers
--------------------------------
- [ PEGs and the Structure of Languages ]( https://blog.bruce-hill.com/pegs-and-the-structure-of-languages )
- [ Packrat Parsing from Scratch ]( https://blog.bruce-hill.com/packrat-parsing-from-scratch )
