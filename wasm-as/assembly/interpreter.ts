import { JSON } from "assemblyscript-json/assembly"
import * as builtins from "./builtins.ts"
import { ArgumentList, TychonMacro } from "./constants.ts"
import { Dictionary } from "./Dictionary.ts"
import { TyValue, TyList, TyNumber, TyString } from "./TyValue"

export function evaluateJson(codeJson: string): string {
  // console.log('!!! Tychon evaluator')
  const scope = new Dictionary()

  let listOfExpressions: TyList = TyValue.parseJSON(codeJson) as TyList
  return evaluate(scope, listOfExpressions).inspect()
}

export function evaluate(scope: Dictionary, value: TyValue): TyValue {
  // console.log(`!!! evaluate() value=${value.toString()}`)
  if (value instanceof TyList) {
    return call(scope, value as TyList)
  } else {
    return value
  }
}

export function tyEvaluate(scope: Dictionary, args: TyList): TyValue {
  return evaluate(scope, args.get(0))
}

function call(scope: Dictionary, args: ArgumentList):TyValue {
  if (! args instanceof TyList) throw new Error('args should be TyList')

  // input:
  const functionName:TyValue = (args as TyList).get(0)
  const funcArgs = new TyList((args as TyList).slice(1))

  // console.log(`!!! call() functionName = ${functionName}`)
  const func = lookup(scope, (functionName as TyString).nativeString())
  return func(scope, funcArgs)
}

function lookup(scope: Dictionary, functionName: string):TychonMacro {
  if (functionName === "evaluate") return tyEvaluate
  if (functionName === "print") return builtins.print
  if (functionName === "module") return builtins.module
  if (functionName === "define") return builtins.define
  if (functionName === "symbol") return builtins.symbol
  if (functionName === "Symbol") return builtins.symbol

  return builtins.print
}

