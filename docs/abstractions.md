# Abstractions in Tychos
aka Interfaces, or Abstract Base Classes

## Sequence / Iteration

- a.map( fn )
- a.each( fn )
- a.zip( fn )
- a.iterator() — returns an Iterator object which has:
    .start() — returns first value or raises StopIteration
    .next() — returns next value or raises StopIteration

## Container
- a.contains(b) = True if object 'a' contains 'b'

   my_dictionary.contains("my_key")
   list_of_animals.contains("duck")

- a.get(b) = retrieves value

### Mutable Container
- a.set(b, c) = set values

## Length
- a.length() = returns the numbeer of things contained in 'a'

## Callable
- a.call(<arg>...)

## Messageable
- a.send(<message> <optional arg> ...)

## Hashing
- a.hash()

## Equality
- a.equals(b)

## Comparison / Ordered
- a.compare(b)
  returns -1 if a < b
  returns 0  if a.equals(b)
  returns 1 if a > b

methods derived from compare():
- a.greater_than(b)
- a.greater_than_or_equal(b)
- a.less_than(b)
- a.less_than_or_equal(b)

## labeled things
labeled-things (Label? nomination? reference? tagged?)
    Can we abstract and generalize these things?
    - A type which contains a 'name' and a 'value'
        - key-values when creating a dictionary
        - function arguments a la Python can be sequential, or labeled?

        - name:value pair when defining a constant or a variable
        - exporting a symbol from your module takes a label:value pair? -- maybe define() returns a
          nomination that can be exported.

    - Things that have names
        - named functions

    a labeled thing:
    - responds to __label__ and __value__

    type:: Label
        name: String
        value: Any

    type:: Function
        name: String
        doc: String
        parameters: [name, doc, type, default]

