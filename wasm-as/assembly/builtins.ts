import { JSON } from "assemblyscript-json/assembly"
import { ArgumentList, TychonFunction, TychonMacro } from "./constants"
import * as tyv from "./TyValue"
import { tyEvaluate, evaluate } from "./interpreter"
import { Dictionary } from "./Dictionary"

export function print(scope: Dictionary, args: ArgumentList):tyv.Value {
  const result = new Array<string>()
  for(let i = 0; i < args.length(); i++) {
    result.push(evaluate(scope, args.get(i)).toString())
  }
  const msg = result.join(' ')
  return new tyv.TyString(msg)
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
  return tyv.TyString.new("")
}
