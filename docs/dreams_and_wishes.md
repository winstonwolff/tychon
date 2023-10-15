# Dreams and Wishes for Tychon

Driving Feature? Who would adopt it?
    - *** Native and nice syntax for JSX like structures
    - *** Scaffolds beginner programmers to building reliable systems / programming in the large
        - separation of concerns
        - de coupling
        - emphasizig pure functions
        - automated testing
        - programming by contract -- programmable types
    - compiles to WebASM. Run it on CloudFlare.
        WHO: Cloudflare
    - embeddable in other people's programs as text editor or graphical block language
        WHO: Zapier, Slack Workflows, Logic AND OR statements, Gitlab or CirceCI yaml, AirTable
    - multi-threading & messaging to take advantage of cores and immutable data

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

Types are programmable
    - Since there is no compilation phase, just an optimization phase, types
      can be programmed like normal code.
    - Type checking means calling a function to see if this is in fact a type.
    - Some optimizations can use type assertions to simplify code or reduce
      memory footprint.

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

SmallTalk like:
    - message oriented programming — parts of your system can operate as separate
      entities, analagous to a network. They interact via sending messages.
        - Why would this be good? Less coupling? It's how 
        - messages could be made via some RPC protocal like JSON-RPC. Then calls
          could actually go across network--it would be the same as on local
          machine.

writing modes
    - Tychon code
    - HTML a la JSX
    - Human text, i.e. documentation
    - executable examples within documentation

# What does the interpreter provide:
- evaluates nodes of the program
- ALU: math, e.g. + - * / ^
    - primitives
- CPU: Memory allocation
    - Fundamental data types
    - Object
        - List
        - String
        - Dictionary
        - ArgList
    - Macro
- I/O:
  - network access
  - DOM access
  - stdin, stdout, stderr
