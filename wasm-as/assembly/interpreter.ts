import { JSON } from "assemblyscript-json/assembly"
import { lookup } from "./builtins.ts"
import { ArgumentList } from "./constants.ts"
import { LayeredDictionary } from "./LayeredDictionary.ts"

export function evaluate(code: string): string {
  const scope = new LayeredDictionary()
  let v: JSON.Arr = <JSON.Arr>(JSON.parse(code));
  // console.log(`!!! evaluate() code = ${v.stringify()}`)
  return call(scope, v).toString()
}

export function evalValue(scope: LayeredDictionary, value: JSON.Value): JSON.Value {
  // console.log(`!!! evalValue() value=${value.toString()}`)
  if (value.isArr) {
    return call(scope, <JSON.Arr>value)
  } else {
    return value
  }
}

function call(scope: LayeredDictionary, args: JSON.Arr):JSON.Value {
  const a = args.valueOf()
  const functionName = a[0].toString()
  const funcArgs = a.slice(1)

  // console.log(`!!! call() functionName = ${functionName}`)
  const func = lookup(scope, functionName)
  return func(funcArgs)
}

function send(args: ArgumentList): JSON.Value {
  // inputs:
  const obj = args[0]
  const methodName = args[1]
  const methodArgs = args.slice(2)

  const func = obj[methodName]
  obj.apply(obj, methodName, methodArgs)
}

