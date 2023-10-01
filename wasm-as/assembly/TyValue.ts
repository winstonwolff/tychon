import { JSON } from "assemblyscript-json/assembly"

export class TyValue {

  static fromJSON(jsonString:string): TyValue {
    return TyValue.fromJsonValue(JSON.parse(jsonString))
  }

  // Convert from JSON.Value's to TyValues
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

  toString(): string { throw new Error("implemented in subclass") }
  inspect(): string { throw new Error("implemented in subclass") }
}

export class TyString extends TyValue {
  value: string = "";

  constructor(s:string) {
    super()
    this.value = s
  }

  // returns e.g. 'abc'
  toString(): string { return this.value }

  // returns e.g. '"abc"'
  inspect(): string { return `TyString("${this.value.toString()}")` }
}

export class TyNumber extends TyValue {
  value: number = 0;

  constructor(n:number) {
    super()
    this.value = n
  }

  toString(): string { return this.value.toString() }
  inspect(): string { return `TyNumber(${this.value.toString()})` }
}

export class TyBoolean extends TyValue {
  value: boolean = false;

  constructor(b:boolean) {
    super()
    this.value = b
  }

  toString(): string { return this.value.toString() }
  inspect(): string { return `TyBoolean(${this.value.toString()})` }
}

export class TyList extends TyValue {
  value: Array<TyValue>

  constructor(list:Array<TyValue>) {
    super()
    this.value = list
  }

  toString(): string {
    const parts: string[] = this.value.map<string>( function(v){ return v.toString() } )
    return `[${parts.join(" ")}]`
  }

  inspect(): string {
    const parts: string[] = this.value.map<string>( function(v){ return v.inspect() } )
    return `TyList(${parts.join(" ")})`
  }
}

