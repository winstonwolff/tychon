import { JSON } from "assemblyscript-json/assembly"
import { ArgumentList } from "./TyValue"
import * as tyv from "./TyValue"

export class Dictionary extends tyv.Value {
  namedValues: Map<string, tyv.Value>

  static new(initValues: Array<Array<tyv.Value>>=[]): Dictionary {
    return new Dictionary(initValues)
  }

  constructor(initValues: Array<Array<tyv.Value>>=[]) {
    super("Dictionary")
    this.namedValues = new Map()

    for(let i = 0; i < initValues.length; i++) {
      this.set(initValues[i][0], initValues[i][1])
    }
  }

  toString(): string {
    return this.namedValues.toString()
  }

  inspect(): string {
    let parts = new Array<string>()
    const keys: Array<string> = this.namedValues.keys()
    const values: Array<tyv.Value> = this.namedValues.values()

    for(let i = 0; i < keys.length; i++) {
      parts.push(`[${keys[i].toString()} ${values[i].inspect()}]`)
    }
    return `Dictionary([ ${parts.join(' ')} ])`
  }

  has(key: tyv.Value): boolean {
    return this.namedValues.has(this._normalizedKey(key))
  }

  // store 'value' under 'key'
  set(key: tyv.Value, value: tyv.Value): tyv.Value {
    this.namedValues.set(this._normalizedKey(key), value)
    return value
  }

  // same as set(), but with Tychon args
  tySet(args: ArgumentList): tyv.Value {
    // inputs:
    const key = (args as tyv.List).get(0)
    const value = (args as tyv.List).get(1)

    this.set(key, value)
    return value
  }

  // Returns the value by 'key'
  get(key: tyv.Value): tyv.Value {
    return this.namedValues.get(this._normalizedKey(key))
  }

  // same as get() but with Tychon args
  tyGet(args: ArgumentList): tyv.Value {
    // inputs:
    const key = (args as tyv.List).get(0) // The key of the value you want

    return this.get(key)
  }

  _normalizedKey(k: tyv.Value): string {
    return k.inspect()
  }
}
