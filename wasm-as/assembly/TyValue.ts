import { JSON } from "assemblyscript-json/assembly"
import { Dictionary } from "./Dictionary"
import { ArgumentList, TychonFunction } from "./constants"
import { ArgumentDescription } from "./ArgumentDescription"
import { evaluate } from "./interpreter"

export class TyValue {
  type_name:string

  constructor(type_name:string="TyValue") {
    this.type_name = type_name
  }

  // Takes a JSON string, and converts to a graph of TyValues
  static parseJSON(jsonString:string): TyValue {
    return TyValue.fromJsonValue(JSON.parse(jsonString))
  }

  // Takes a JSON.Value and converts to TyValues
  static fromJsonValue(v: JSON.Value): TyValue {
    if (v.isString) {
      return new TyString((v as JSON.Str).valueOf())
    }
    if (v.isNum) {
      return new TyNumber((v as JSON.Num).valueOf()) 
    }
    if (v.isBool) {
      return new TyBoolean((v as JSON.Bool).valueOf()) 
    }
    if (v.isArr) {
      const arr: Array<JSON.Value> = (v as JSON.Arr).valueOf()
      const list: Array<TyValue> = []
      for(let i = 0; i < arr.length; i++ ) {
        list.push(TyValue.fromJsonValue(arr[i]))
      }

      return new TyList(list)
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

export const tyString = (s: string):TyValue => new TyString(s)
export class TyString extends TyValue {
  value: string = "";

  constructor(s:string) {
    super("TyString")
    this.value = s
  }

  // return AssemblyScript value
  nativeString(): string { return this.value }

  // returns e.g. 'abc'
  toString(): string { return this.value }

  // returns e.g. '"abc"'
  inspect(): string { return `TyString("${this.value.toString()}")` }

  instance_of(): TyBool { throw new Error(`not implemented in ${this.class.name}`) }
}

export const tyNumber = (n: number):TyValue => new TyNumber(n)
export class TyNumber extends TyValue {
  value: number = 0;

  constructor(n:number) {
    super("TyNumber")
    this.value = n
  }

  // return AssemblyScript value
  nativeFloat(): f64 { return this.value }
  nativeInteger(): i32 { return Math.round(this.value) as i32 }

  toString(): string { return this.value.toString() }
  inspect(): string { return `TyNumber(${this.value.toString()})` }
}

export class TyBoolean extends TyValue {
  value: boolean = false;

  constructor(b:boolean) {
    super("TyBoolean")
    this.value = b
  }

  // return AssemblyScript value
  nativeBoolean(): boolean { return this.value }

  toString(): string { return this.value.toString() }
  inspect(): string { return `TyBoolean(${this.value.toString()})` }
}

export const TyTrue = new TyBoolean(true)
export const TyFalse = new TyBoolean(false)

export const tyList = (list: Array<TyValue> = []):TyList => new TyList(list)
export class TyList extends TyValue {
  arrayOfValues: Array<TyValue>

  constructor(list:Array<TyValue> = []) {
    super("TyList")
    this.arrayOfValues = list
  }

  toString(): string {
    const parts: string[] = this.arrayOfValues.map<string>( function(v){ return v.toString() } )
    return `[${parts.join(" ")}]`
  }

  inspect(): string {
    const parts: string[] = this.arrayOfValues.map<string>( function(v){ return v.inspect() } )
    return `TyList(${parts.join(" ")})`
  }

  get(index: i32): TyValue {
    return this.arrayOfValues[index]
  }

  tyGet(args: ArgumentList): TyValue {
    // inputs:
    const index: i32 = (args as TyList).get(0).nativeInteger()

    return this.get(index)
  }

  length(): i32 { return this.arrayOfValues.length }
  tyLength(): TyValue { return new TyNumber(this.length()) }

  slice(startIndex: i32): Array<TyValue> {
    return this.arrayOfValues.slice(startIndex)
  }

  append(v: TyValue): TyValue {
    this.arrayOfValues.push(v)
    return this
  }

  tySlice(args: ArgumentList): TyList {
    // inputs:
    const index = (args as TyList).get(new TyNumber(0)).nativeInteger()

    return new TyList(this.slice(index))
  }

  map(callback: (v: TyValue, index:i32, self:Array<TyValue>)=>TyValue): Array<TyValue> {
    return this.arrayOfValues.map(callback)
  }

  tyMap(callback: TychonFunction): TyList {
    const result = new TyList()
    for(let i=0; i < this.arrayOfValues.length; i++) {
      result.append(callback(new TyList([this.arrayOfValues[i]])))
    }
    return result
  }

  any( is_true: (value: TyValue, index: i32, self: Array<TyValue>) => boolean ): boolean {
    return this.arrayOfValues.some(is_true)
  }
}

export const tyMacro = (name:string, argDesc:ArgumentDescription, code: TyValue):TyMacro =>
  ( new TyMacro(name, argDesc, code) )
export class TyMacro extends TyValue {
  name: string
  argDesc: ArgumentDescription
  code: TyValue

  constructor(name:string, argDesc:ArgumentDescription, code: TyValue ) {
    super("TyMacro")
    this.name = name
    this.argDesc = argDesc
    this.code = code
  }

  toString(): string {
    return this.inspect()
  }

  inspect(): string {
    return `TyMacro(${this.name})`
  }

  call(args: ArgumentList): TyValue {
    this.argDesc.throw_if_invalid(args)
    // inputs:
    const scope = args.get(0) as Dictionary

    return evaluate(scope, this.code)
  }
}
