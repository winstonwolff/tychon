# Tychon — An experiment in a python-y smalltalk-y lisp-y embedded language.

Usage
-----
  ./run_tests.sh                        # run the tests
  ./tychon.py <sourcefile>.ty           # execute a source file
  ./tychon.py                           # a REPL


Driving Features
----------------

    - **Scaffolds beginner programmers** to building reliable systems / programming in the large

        - separation of concerns
            - network
            - db
            - view

        - de coupling

        - emphasizing pure functions

        - automated testing

        - programming by contract -- programmable types

        - **Overview of system** integrated documation so new developer can get overview of
          system without reviewing every file.

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


    Functional
        - mostly immutable data structures like Clojure
        - "functions" are pure, and are clearly marked
        - dot-lookup of functions that operate on immutable data structures, e.g.
            def:: Person
                 Record::
                    name: String
                    phone: Integer
                    set_phone: pure func(person new_phone):: <implementation returns new Person>
            p = Person(name: 'joe')
            p = p.set_phone('415 555 1212')


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
