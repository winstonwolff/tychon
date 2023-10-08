# Abstractions in Tychos
aka Interfaces, or Abstract Base Classes

## Sequence / Iteration

- a.map( fn )
- a.each( fn )
- a.zip( fn )

## Container
- a.contains(b) = True if object 'a' contains 'b'

   my_dictionary.contains("my_key")
   list_of_animals.contains("duck")

- a.get(b) = retrieves value
- a.set(b, c) = set values, but only for mutable containers


## Length

- a.length() = returns the numbeer of things contained in 'a'

## Callable

- a.call(<arg>...)

## Messageable

- a.send(<message> <optional arg> ...)

## Equality

- a.equals(b)

## Hashing

- a.hash()

## Comparison

- a.compare(b)
  returns -1 if a < b
  returns 0  if a.equals(b)
  returns 1 if a > b

methods derived from compare():
- a.greater_than(b)
- a.greater_than_or_equal(b)
- a.less_than(b)
- a.less_than_or_equal(b)
