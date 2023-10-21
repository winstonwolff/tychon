# Tychon — An experiment in a python-y smalltalk-y lisp-y embedded language.

Python Parser Usage
-------------------
  ./run_tests.sh                        # run the tests
  ./tychon.py <sourcefile>.ty           # execute a source file
  ./tychon.py                           # a REPL

### Developer setup
  pip install -r requirements.txt

Wasm Interpreter Usage
-----------------
  cd wasm-as
  ./runit.sh                            # launch server and compiler
  npm test                              # run unit tests
  npm run test:watch                    # re-run test when a file changes

## Programming language for teams
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


Docs
----
  [ To Do List ]( TODO.md )
  [ Abstractions ]( docs/abstractions.md )

Ideas
-----
  [ Dreams and Wishes ]( docs/dreams_and_wishes.md )
  [ New Functional Lang ]( docs/new_functional_lang.md )
  [ Description Language ]( docs/description_language.md )



References on PEG & Packrat parsers
--------------------------------
- [ PEGs and the Structure of Languages ]( https://blog.bruce-hill.com/pegs-and-the-structure-of-languages )
- [ Packrat Parsing from Scratch ]( https://blog.bruce-hill.com/packrat-parsing-from-scratch )

## References for assembly script
- [ AssemblyScript ](https://www.assemblyscript.org/concepts.html)
- [ TypeScript ](https://www.typescriptlang.org)
- [ AS-pect ](https://as-pect.gitbook.io/as-pect/as-api/expectations)
- [ assemblyscript-json ](https://github.com/near/assemblyscript-json/tree/main/docs)

