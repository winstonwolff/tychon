import { JSON } from "assemblyscript-json/assembly"
import { ArgumentList, TychonFunction } from "./constants"

export class TyValue {

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

export class TyString extends TyValue {
  value: string = "";

  constructor(s:string) {
    super()
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

export class TyNumber extends TyValue {
  value: number = 0;

  constructor(n:number) {
    super()
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
    super()
    this.value = b
  }

  // return AssemblyScript value
  nativeBoolean(): boolean { return this.value }

  toString(): string { return this.value.toString() }
  inspect(): string { return `TyBoolean(${this.value.toString()})` }
}

export const TyTrue = new TyBoolean(true)
export const TyFalse = new TyBoolean(false)

export class TyList extends TyValue {
  arrayOfValues: Array<TyValue>

  constructor(list:Array<TyValue> = []) {
    super()
    this.arrayOfValues = list
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

  map(callback: TychonFunction): Array<TyValue> {
    return this.arrayOfValues.map(callback)
  }

  tyMap(callback: TychonFunction): TyList {
    return new TyList(this.map(callback))
  }

  toString(): string {
    const parts: string[] = this.arrayOfValues.map<string>( function(v){ return v.toString() } )
    return `[${parts.join(" ")}]`
  }

  inspect(): string {
    const parts: string[] = this.arrayOfValues.map<string>( function(v){ return v.inspect() } )
    return `TyList(${parts.join(" ")})`
  }
}

