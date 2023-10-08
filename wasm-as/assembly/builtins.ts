import { JSON } from "assemblyscript-json/assembly"
import { ArgumentList, TychonFunction, TychonMacro } from "./constants"
import { TyValue, TyString, TyList } from "./TyValue"
import { evalValue } from "./interpreter"
import { Dictionary } from "./Dictionary"

export function lookup(scope: Dictionary, functionName: string):TychonMacro {
  if (functionName === "print") return print
  // if (functionName === "list") return list
  if (functionName === "module") return module
  // if (functionName === "define") return define(scope)

  return print
}

function print(scope: Dictionary, args: ArgumentList):TyValue {
  const msg = args.toString()
  // const msg:string = (args as TyList)
  //   .map( function(v: TyValue): TyList { return v.toString() })
  //   .join(" ")

  // console.log(`!!! print msg= "${msg}"`)
  return new TyString(msg)
}

// function list( args:ArgumentList ):TyValue {
//   const msg = args.toString()
//   const result = new JSON.Arr()
//   for(let i = 0; i < args.length; i++) {
//     result.push(args[i])
//   }

//   return result
// }

function module(scope: Dictionary, args:ArgumentList): TyValue {
  // const result = (args as TyList).map( function(v) { return evalValue(scope, v) } )
  const result = new Array<TyValue>()
  for(let i = 0; i < (args as TyList).length(); i++) {
    result.push(evalValue(scope, (args as TyList).get(i)))
  }
  return new TyList(result)
}

export function zip(_unused: Dictionary, seq_1: TyList, seq_2: TyList): TyList {
  if (seq_1.length() != seq_2.length()) throw new Error('Sequences must be the same length.')
  const result = new TyList()
  for(let i = 0; i < seq_1.length(); i++) {
    result.append( new TyList([seq_1.get(i), seq_2.get(i)]) )
  }
  return result
}

// function define(scope: Dictionary): TychonFunction {
//   return function(args: ArgumentList): TyValue {
//     // inputs:
//     const name = args[0]
//     const value = args[1]
//     if (! scope instanceof Dictionary) throw new Error("Invalid args")
//     if (! name instanceof Dictionary) throw new Error("Invalid args")

//     scope.set([name, value])
//     scope.inspect()
//   }
// }

// Conveniently call both AS functions and Tychon functions with one syntax.
function call(scope: Dictionary, args: ArgumentList): TyValue {
  // inputs

}
