import { JSON } from "assemblyscript-json/assembly"
import { TychonFunction, TychonMacro } from "./constants"
import { ArgumentList } from "./TyValue"
import { ArgumentDescription } from "./ArgumentDescription"
import * as tyv from "./TyValue"
import { evaluate } from "./interpreter"
import { Dictionary } from "./Dictionary"

export function print(scope: Dictionary, args: ArgumentList):tyv.Value {
  const result = new Array<string>()
  for(let i = 0; i < args.length(); i++) {
    result.push(evaluate(scope, args.get(i)).toString())
  }
  const msg = result.join(' ')
  return new tyv.String(msg)
}

export function module(scope: Dictionary, args:ArgumentList): tyv.Value {
  const result = new Array<tyv.Value>()
  for(let i = 0; i < (args as tyv.List).length(); i++) {
    result.push(evaluate(scope, args.get(i)))
  }
  return new tyv.List(result)
}

export function zip(_unused: null | Dictionary, seq_1: tyv.List, seq_2: tyv.List): tyv.List {
  if (seq_1.length() != seq_2.length()) throw new Error('Sequences must be the same length.')
  const result = new tyv.List()
  for(let i = 0; i < seq_1.length(); i++) {
    result.append( new tyv.List([seq_1.get(i), seq_2.get(i)]) )
  }
  return result
}

export function define(scope: Dictionary, args: ArgumentList): tyv.Value {
  // inputs:
  const name = args.get(0)
  const value = args.get(1)

  scope.tySet(args)
  return value
}

export function symbol(scope: Dictionary, args: ArgumentList): tyv.Value {
  return scope.tyGet(args)
}

export function noop(scope: Dictionary, args: ArgumentList): tyv.Value {
  return tyv.String.new("")
}

// Macro which creates and returns new Macros
export const MacroMacro = tyv.NativeMacro.new(
  "Macro",
  ArgumentDescription.ofArray([
    ['name', 'String'],
    ['argList', 'List'],
    ['code', 'List']
  ]),
  (scope: Dictionary, args: ArgumentList): tyv.Value => {
    const name = args.get(0).nativeString()
    const argDesc = ArgumentDescription.new(ArgumentList.ofList(args.get(1) as tyv.List))
    const code = args.get(2)

    return tyv.Macro.new(name, argDesc, code)
  }
)

export const BUILTINS = Dictionary.new([
  // [ tyv.String.new("evaluate"),
  //   tyv.NativeMacro.new('evaluate',
  //     ArgumentDescription.ofArray([['value', 'Value']]),
  //     (scope: Dictionary, args: ArgumentList): tyv.Value => evaluate(scope, args.get(0))
  //   )
  // ],
  [tyv.String.new("Macro"), MacroMacro],
])

