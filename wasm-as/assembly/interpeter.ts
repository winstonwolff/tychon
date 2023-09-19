import { JSON } from "assemblyscript-json/assembly"

export function evaluate(code: string): string {
  console.log('evaluate called')
  console.log(`string="${code}"`)

  let v: JSON.Arr = <JSON.Arr>(JSON.parse(code));
  console.log(`v = ${v.stringify()}`)
  console.log(`v.isArr = ${v.isArr}`)
  console.log(`v.isObj = ${v.isObj}`)
  console.log(`??? = ${v.valueOf()[0]}`)
  return call(v.valueOf()).toString()
}

function call(a: Array<JSON.Value>):JSON.Value {
  const f = lookup(a[0])
  return f(a.slice(1))
}

type List = Array<JSON.Value>
type AnyFunc = (l:List) => JSON.Value

function lookup(functionName:JSON.Value):AnyFunc {
  // switch(functionName.valueOf()) {
  //   case "print": return print
  // }
  return print
}

function print(arguments:List):JSON.Value {
  const msg = arguments.toString()
  console.log(msg)
  return new JSON.Str(msg)
}
