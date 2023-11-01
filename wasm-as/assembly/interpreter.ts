import { JSON } from "assemblyscript-json/assembly"
import * as builtins from "./builtins.ts"
import { ArgumentList } from "./TyValue"
import { TychonMacro } from "./constants.ts"
import { Dictionary } from "./Dictionary.ts"
import { ArgumentDescription } from "./ArgumentDescription.ts"
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
    return call(scope, ArgumentList.ofList(<tyv.List>value))
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
  const functionName:tyv.Value = args.get(0)
  const funcArgs = ArgumentList.new(args.slice(1))

  if (builtins.BUILTINS.has(functionName)) {
    const macro = builtins.BUILTINS.get(functionName)
    if (macro.type_name == 'Macro') {
      return (macro as tyv.Macro).__call__(scope, funcArgs)
    } else if (macro.type_name == 'NativeMacro') {
      return (macro as tyv.NativeMacro).__call__(scope, funcArgs)
    }
    throw new Error(`unknown type for macro ${functionName} ${macro.type_name}`)
  }

  const fn = (functionName as tyv.String).nativeString()
  const func = lookup(scope, fn)
  return func(scope, funcArgs)
}

function lookup(scope: Dictionary, functionName: string):TychonMacro {
  if (functionName === "evaluate") return tyEvaluate
  if (functionName === "print") return builtins.print
  if (functionName === "module") return builtins.module
  if (functionName === "define") return builtins.define
  if (functionName === "symbol") return builtins.symbol
  if (functionName === "Symbol") return builtins.symbol

  return builtins.noop
}

