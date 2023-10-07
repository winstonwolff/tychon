import { JSON } from "assemblyscript-json/assembly"
import { lookup } from "./builtins.ts"
import { ArgumentList } from "./constants.ts"
import { Dictionary } from "./Dictionary.ts"
import { TyValue, TyList, TyNumber, TyString } from "./TyValue"

export function evaluate(codeJson: string): string {
  // console.log('!!! Tychon evaluator')
  const scope = new Dictionary()

  let listOfExpressions: TyList = TyValue.parseJSON(codeJson) as TyList
  return call(scope, listOfExpressions).inspect()
}

export function evalValue(scope: Dictionary, value: TyValue): TyValue {
  // console.log(`!!! evalValue() value=${value.toString()}`)
  if (value instanceof TyList) {
    return call(scope, value as TyList)
  } else {
    return value
  }
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

// function send(args: ArgumentList): TyValue {
//   // inputs:
//   const obj = args[0]
//   const methodName = args[1]
//   const methodArgs = args.slice(2)

//   const func = obj[methodName]
//   obj.apply(obj, methodName, methodArgs)
// }

