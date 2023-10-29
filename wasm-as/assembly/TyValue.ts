import { JSON } from "assemblyscript-json/assembly"
import { Dictionary } from "./Dictionary"
import { TychonFunction, TychonMacro } from "./constants"
import { ArgumentDescription } from "./ArgumentDescription"
import { evaluate } from "./interpreter"

export class Value {
  type_name:string

  constructor(type_name:string="Value") {
    this.type_name = type_name
  }

  // Takes a JSON string, and converts to a graph of Values
  static parseJSON(jsonString:string): Value {
    return Value.fromJsonValue(JSON.parse(jsonString))
  }

  // Takes a JSON.Value and converts to Values
  static fromJsonValue(v: JSON.Value): Value {
    if (v.isString) {
      return new String((v as JSON.Str).valueOf())
    }
    if (v.isNum) {
      return new Number((v as JSON.Num).valueOf()) 
    }
    if (v.isBool) {
      if (v as JSON.Bool) return True
      else return False
    }
    if (v.isArr) {
      const arr: Array<JSON.Value> = (v as JSON.Arr).valueOf()
      const list: Array<Value> = []
      for(let i = 0; i < arr.length; i++ ) {
        list.push(Value.fromJsonValue(arr[i]))
      }

      return new List(list)
    }
    throw new Error(`bad value: ${v} type:${typeof(v)}`)
  }

  // return AssemblyScript value
  // nativeString(): string { throw new Error("implemented in subclass") }
  nativeString(): string { throw new Error(`not implemented in '${typeof(this)}'`) }
  nativeFloat(): f64 { throw new Error(`not implemented in '${typeof(this)}'`) }
  nativeInteger(): i32 { throw new Error(`not implemented in '${typeof(this)}'`) }
  nativeBoolean(): bool { throw new Error(`not implemented in '${typeof(this)}'`) }

  toString(): string { throw new Error(`not implemented in '${typeof(this)}'`) }

  inspect(): string { throw new Error(`not implemented in '${typeof(this)}'`) }
}

export class String extends Value {
  value: string = "";

  constructor(s:string) {
    super("String")
    this.value = s
  }

  static new(s: string):Value { return new String(s) }

  // return AssemblyScript value
  nativeString(): string { return this.value }

  // returns e.g. 'abc'
  toString(): string { return this.value }

  // returns e.g. '"abc"'
  inspect(): string { return `String("${this.value.toString()}")` }

  instance_of(): Boolean { throw new Error(`not implemented in ${this.class.name}`) }
}

export class Number extends Value {
  value: number = 0;

  static new(n: number):Value { return new Number(n) }

  constructor(n:number) {
    super("Number")
    this.value = n
  }

  // return AssemblyScript value
  nativeFloat(): f64 { return this.value }
  nativeInteger(): i32 { return Math.round(this.value) as i32 }

  toString(): string { return this.value.toString() }
  inspect(): string { return `Number(${this.value.toString()})` }
}

export class Boolean extends Value {
  value: boolean = false;

  constructor(b:boolean) {
    super("Boolean")
    this.value = b
  }

  // return AssemblyScript value
  nativeBoolean(): boolean { return this.value }

  toString(): string { return this.value.toString() }
  inspect(): string { return `Boolean(${this.value.toString()})` }
}

export const True = new Boolean(true)
export const False = new Boolean(false)

export class List extends Value {
  arrayOfValues: Array<Value>

  static new(list: Array<Value> = []):List {
    return new List(list)
  }

  constructor(list:Array<Value> = []) {
    super("List")
    this.arrayOfValues = list
  }

  toString(): string {
    const parts: string[] = this.arrayOfValues.map<string>( function(v){ return v.toString() } )
    return `[${parts.join(" ")}]`
  }

  inspect(): string {
    const parts: string[] = this.arrayOfValues.map<string>( function(v){ return v.inspect() } )
    return `List(${parts.join(" ")})`
  }

  get(index: i32): Value {
    return this.arrayOfValues[index]
  }

  tyGet(args: ArgumentList): Value {
    // inputs:
    const index: i32 = (args as List).get(0).nativeInteger()

    return this.get(index)
  }

  length(): i32 { return this.arrayOfValues.length }
  tyLength(): Value { return new Number(this.length()) }

  slice(startIndex: i32): Array<Value> {
    return this.arrayOfValues.slice(startIndex)
  }

  append(v: Value): Value {
    this.arrayOfValues.push(v)
    return this
  }

  tySlice(args: ArgumentList): List {
    // inputs:
    const index = (args as List).get(new Number(0)).nativeInteger()

    return new List(this.slice(index))
  }

  map(callback: (v: Value, index:i32, self:Array<Value>)=>Value): Array<Value> {
    return this.arrayOfValues.map(callback)
  }

  tyMap(callback: TychonFunction): List {
    const result = new List()
    for(let i=0; i < this.arrayOfValues.length; i++) {
      result.append(callback(ArgumentList.new([this.arrayOfValues[i]])))
    }
    return result
  }

  any( is_true: (value: Value, index: i32, self: Array<Value>) => boolean ): boolean {
    return this.arrayOfValues.some(is_true)
  }
}


export class ArgumentList extends List {
  static new(list: Array<Value> = []):ArgumentList {
    return new ArgumentList(list)
  }

  static ofList(list: List):ArgumentList {
    return ArgumentList.new(list.arrayOfValues)
  }
}


export class Macro extends Value {
  name: string
  argDesc: ArgumentDescription
  code: Value

  static new(name:string, argDesc:ArgumentDescription, code: Value):Macro { return new Macro(name, argDesc, code) }

  constructor(name:string, argDesc:ArgumentDescription, code: Value ) {
    super("Macro")
    this.name = name
    this.argDesc = argDesc
    this.code = code
  }

  toString(): string {
    return this.inspect()
  }

  inspect(): string {
    return `Macro(${this.name})`
  }

  call(scope:Dictionary, args: ArgumentList): Value {
    this.argDesc.throw_if_invalid(args)
    return evaluate(scope, this.code)
  }
}

// Macro which creates and returns new Macros
// export const MacroMacro = Macro.new("Macro",


export class NativeMacro extends Value {
  name: string
  argDesc: ArgumentDescription
  assemblyScriptFunction: TychonMacro

  static new(name:string, argDesc:ArgumentDescription, assemblyScriptFunction: TychonMacro): NativeMacro {
    return new NativeMacro(name, argDesc, assemblyScriptFunction)
  }

  constructor(name:string, argDesc:ArgumentDescription, assemblyScriptFunction: TychonMacro) {
    super("NativeMacro")
    this.name = name
    this.argDesc = argDesc
    this.assemblyScriptFunction = assemblyScriptFunction
  }

  toString(): string {
    return this.inspect()
  }

  inspect(): string {
    return `NativeMacro(${this.name})`
  }

  call(scope: Dictionary, args: ArgumentList): Value {
    this.argDesc.throw_if_invalid(args)
    return this.assemblyScriptFunction(scope, args)
  }
}
