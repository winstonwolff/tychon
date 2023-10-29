import { JSON } from "assemblyscript-json/assembly"
import * as builtins from "./builtins.ts"
import { ArgumentList, TychonMacro } from "./constants.ts"
import { Dictionary } from "./Dictionary.ts"
import * as tyv from "./TyValue"

export function evaluateJson(codeJson: string): string {
  // console.log('!!! Tychon evaluator')
  const scope = new Dictionary()

  let listOfExpressions: tyv.List = tyv.Value.parseJSON(codeJson) as tyv.List
  return evaluate(scope, listOfExpressions).inspect()
}

export function evaluate(scope: Dictionary, value: tyv.Value): tyv.Value {
  // console.log(`!!! evaluate() value=${value.toString()}`)
  if (value instanceof tyv.List) {
    return call(scope, value as tyv.List)
  } else {
    return value
  }
}

export function tyEvaluate(scope: Dictionary, args: ArgumentList): tyv.Value {
  return evaluate(scope, args.get(0))
}

function call(scope: Dictionary, args: ArgumentList):tyv.Value {
  if (! args instanceof tyv.List) throw new Error('args should be List')

  // input:
  const functionName:tyv.Value = (args as tyv.List).get(0)
  const funcArgs = new tyv.List((args as tyv.List).slice(1))

  // console.log(`!!! call() functionName = ${functionName}`)
  const func = lookup(scope, (functionName as tyv.String).nativeString())
  return func(scope, funcArgs)
}

function lookup(scope: Dictionary, functionName: string):TychonMacro {
  if (functionName === "evaluate") return tyEvaluate
  if (functionName === "print") return builtins.print
  if (functionName === "module") return builtins.module
  if (functionName === "define") return builtins.define
  if (functionName === "symbol") return builtins.symbol
  if (functionName === "Symbol") return builtins.symbol
  // if (functionName === "Macro") return Macro.new

  return builtins.noop
}

