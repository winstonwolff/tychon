import { JSON } from "assemblyscript-json/assembly"

function call(args: JSON.Arr):JSON.Value {
  const a = args.valueOf()
  const functionName = a[0].toString()
  console.log(`!!! call() functionName = ${functionName}`)
  const f = lookup(functionName)
  return f(a.slice(1))
}

function evalValue(value: JSON.Value): JSON.Value {
  console.log(`!!! evalValue() value=${value.toString()}`)
  if (value.isArr) {
    return call(<JSON.Arr>value)
  } else {
    return value
  }
}

export function evaluate(code: string): string {
  let v: JSON.Arr = <JSON.Arr>(JSON.parse(code));
  console.log(`!!! evaluate() code = ${v.stringify()}`)
  return call(v).toString()
}

type List = Array<JSON.Value>
type AnyFunc = (l:List) => JSON.Value


function print(arguments:List):JSON.Value {
  const msg = arguments.toString()
  console.log("!!! print msg="); console.log(msg)
  return JSON.from(msg)
}

function list(arguments:List):JSON.Value {
  const msg = arguments.toString()
  console.log('!!! list() msg='); console.log(msg)
  const result = new JSON.Arr()
  for(let i = 0; i < arguments.length; i++) {
    result.push(arguments[i])
  }

  return result
}

function mod(arguments:List): JSON.Value {
  const result = new JSON.Arr()
  for(let i = 0; i < arguments.length; i++) {
    result.push(evalValue(arguments[i]))
  }
  return result
}

type TyValue = JSON.Value
type TyFunction = (args:List) => TyValue

function lookup(functionName: string): TyFunction {
  if (functionName === "print") return print
  if (functionName === "list") return list
  if (functionName === "mod") return mod

  return print
}

