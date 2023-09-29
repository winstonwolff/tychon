import { JSON } from "assemblyscript-json/assembly"


type List = Array<JSON.Value>
type ArgumentList = Array<JSON.Value>
type TyFunction = (args:ArgumentList) => JSON.Value

export function evaluate(code: string): string {
  let v: JSON.Arr = <JSON.Arr>(JSON.parse(code));
  // console.log(`!!! evaluate() code = ${v.stringify()}`)
  return call(v).toString()
}

function evalValue(value: JSON.Value): JSON.Value {
  // console.log(`!!! evalValue() value=${value.toString()}`)
  if (value.isArr) {
    return call(<JSON.Arr>value)
  } else {
    return value
  }
}

function call(args: JSON.Arr):JSON.Value {
  const a = args.valueOf()
  const functionName = a[0].toString()
  // console.log(`!!! call() functionName = ${functionName}`)
  const f = lookup(functionName)
  return f(a.slice(1))
}

function lookup(functionName: string): TyFunction {
  if (functionName === "print") return print
  if (functionName === "list") return list
  if (functionName === "module") return module

  return print
}

function print(arguments: ArgumentList):JSON.Value {
  // const msg = arguments.toString()
  const msg:string = arguments.map<string>( function(v){ return v.toString() } ).join(" ")

  console.log(`!!! print msg= "${msg}"`)
  return JSON.from(msg)
}

function list( arguments:ArgumentList ):JSON.Value {
  const msg = arguments.toString()
  // console.log('!!! list() msg='); console.log(msg)
  const result = new JSON.Arr()
  for(let i = 0; i < arguments.length; i++) {
    result.push(arguments[i])
  }

  return result
}

function module(arguments:ArgumentList): JSON.Value {
  const result = new JSON.Arr()
  for(let i = 0; i < arguments.length; i++) {
    result.push(evalValue(arguments[i]))
  }
  return result
}
