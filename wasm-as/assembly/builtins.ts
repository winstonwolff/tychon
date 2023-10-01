import { JSON } from "assemblyscript-json/assembly"
import { List, ArgumentList, TychonFunction } from "./constants"
import { evalValue } from "./interpreter"
import { LayeredDictionary } from "./LayeredDictionary"

export function lookup(scope: LayeredDictionary, functionName: string): TychonFunction {
  if (functionName === "print") return print
  if (functionName === "list") return list
  if (functionName === "module") return module
  if (functionName === "define") return define(scope)

  return print
}

function print(arguments: ArgumentList):TyValue {
  // const msg = arguments.toString()
  const msg:string = arguments.map<string>( function(v){ return v.toString() } ).join(" ")

  console.log(`!!! print msg= "${msg}"`)
  return JSON.from(msg)
}

function list( arguments:ArgumentList ):TyValue {
  const msg = arguments.toString()
  // console.log('!!! list() msg='); console.log(msg)
  const result = new JSON.Arr()
  for(let i = 0; i < arguments.length; i++) {
    result.push(arguments[i])
  }

  return result
}

function module(arguments:ArgumentList): TyValue {
  const result = new JSON.Arr()
  for(let i = 0; i < arguments.length; i++) {
    result.push(evalValue(arguments[i]))
  }
  return result
}

function define(scope: LayeredDictionary): TychonFunction {
  return function(args: ArgumentList): TyValue {
    // inputs:
    const name = args[0]
    const value = args[1]
    if (! scope instanceof LayeredDictionary) throw new Error("Invalid args")
    if (! name instanceof LayeredDictionary) throw new Error("Invalid args")

    scope.set([name, value])
    scope.inspect()
  }
}
