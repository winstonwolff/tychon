import { JSON } from "assemblyscript-json/assembly"
import { ArgumentList, TychonFunction, TychonMacro } from "./constants"
import { tyList, TyValue, TyString, TyList, TyFalse } from "./TyValue"
import { tyEvaluate, evaluate } from "./interpreter"
import { Dictionary } from "./Dictionary"

export function print(scope: Dictionary, args: ArgumentList):TyValue {
  const result = new Array<string>()
  for(let i = 0; i < args.length(); i++) {
    result.push(evaluate(scope, args.get(i)).toString())
  }
  const msg = result.join(' ')
  return new TyString(msg)
}

export function module(scope: Dictionary, args:ArgumentList): TyValue {
  const result = new Array<TyValue>()
  for(let i = 0; i < (args as TyList).length(); i++) {
    result.push(evaluate(scope, args.get(i)))
  }
  return new TyList(result)
}

export function zip(_unused: null | Dictionary, seq_1: TyList, seq_2: TyList): TyList {
  if (seq_1.length() != seq_2.length()) throw new Error('Sequences must be the same length.')
  const result = new TyList()
  for(let i = 0; i < seq_1.length(); i++) {
    result.append( new TyList([seq_1.get(i), seq_2.get(i)]) )
  }
  return result
}

export function define(scope: Dictionary, args: ArgumentList): TyValue {
  // inputs:
  const name = args.get(0)
  const value = args.get(1)

  scope.tySet(args)
  return value
}

export function symbol(scope: Dictionary, args: ArgumentList): TyValue {
  return scope.tyGet(args)
}

