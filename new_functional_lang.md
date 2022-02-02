New Functional Language
=======================
vim: tabstop=2:softtabstop=2:shiftwidth=2

Want (top priority first):
- can program compiler, to do things like:
  - enforce input and output types at compile time or runtime
  - define a "Type", i.e. something that enforces use at compile and runtime
  - enforce access across modules, e.g.
        * controller knows about view and model
        * view knows about model
        * model cannot know view or controller.
    - or only modules marked 'global-unsafe' can modify global variables.
  - A function may not modify globals unless it is marked.
  - A DSL for specs
- coffeescript-like notation
- nice notation for tree & xml structures
- block based language for building data structures (which can also be programs)


## Enforcing types

    double = (a: int): int -> 2 * a
compiles to:
    (set 'double'
        (function (
            inputs: ((a int))
            return_type: int
            implementation:
                (multiply 2 a)
            )
        )
    )

## What can a Type do?
- convert an AST to a value and back



```
family_tree = List:         # colons indicate the next line begins a list
  ['mary', [ 'misha', 'magdelene' ]]
  'jane', List:
    'jimmy'
    'janet'
  'frank', [
    'freddie'
    'fiona' ]

say_hello = |name, children| ->
  print("hello", name)
  children.map(say_hello)

family_tree.map(say_hello)
```


## Convey a tree structure

html
  body
    div.contents#my-id
      form
        input(id='blah', value='blah')
        input(a, b) where a:
          id='blah'
          value='blah'


## Just a symbol language--execute it yourself

wisp:
  (set add func ((a Number) (b Number)) (+ a a))

  add := func:
      a Number
      b Number
  : (+ a a)

  func main ():
    add 1 1
    add 2 4

  run main

---
  # Setting values
  (set my_int 3)
  set my_int 3 # same as above
  my_int := 3 # same as above

  set my_string "hello"

  (set my_array (Array 1 4 9))
  set my_array (Array 1 4 9)
  set my_array: Array 1 4 9
  set my_array:
    Array 1 4 9
  set my_array:
    Array
      1
      4
      9

  (set my_dict (Dict (one 1) (two 2)))
  (set my_dict
    (Dict
      (one 1)
      (two 2)
    )
  )
  set my_dict:
    Dict:
      "one" 1
      "two" 2

  (cond
    ((== a 1) "one")
    ((== a 2) "two")
    (true "other")
  )

  cond
    eq a 1: "one"
    eq a 2: "two"
    True: "other"
    

---

wisp:
  (import "./jsx" *)
  (set MyList (func (props) (
    (set a (len props.list_of_items))
    (map props.list_of_items
      (func (item_name)
        (jsx
          (li (style: STYLES.li)
              item_name
  )))))))

  import "./jsx" *

  MyList := func (props):
    a := len props.list_of_items
    map props.list_of_items
      func (item_name)
        jsx
          li (style: {STYLES.li}):
            item_name


## Parsing Rules:

- strings are surrounded by " or '
- multiline strings are surrounded by ''' or """
- comments start with #
- multiline comments surrounded by ###
- names are: a-z A-Z 0-9 _ $ '
- numbers have their usual format, e.g. 77, 3.14, -3e08, 0x2bad
- Lists can use various symbols, e.g. [] () {} <>
- Identation from the previous line means the previous list continues, but it's a new sub-list. These are equivalent:
    (a (b c) (d e))
    a
      b c
      d e

- vertical bar as first character means it continues previous line and does not start sub-list

    (a b c d)

    a b
      | d e

    a
    b
    c
    d

- Colons indicate a new list is starting.
    a b c : d e f
  ??? should that mean:
    ((a b c) (d e f))
  or
    (a b c (d e f))

- `:` can be a pairing operator, it makes a tuple.
  `blah: foo` is the same as `(blah foo)`


##






