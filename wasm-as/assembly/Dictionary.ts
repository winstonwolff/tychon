import { JSON } from "assemblyscript-json/assembly"
import { ArgumentList } from "./constants.ts"
import * as tyv from "./TyValue"

export class Dictionary extends tyv.Value {
  namedValues: Map<string, tyv.Value>

  constructor() {
    super("Dictionary")
    this.namedValues = new Map()
  }

  toString(): string {
    return this.namedValues.toString()
  }

  inspect(): string {
    return `Dictionary( ${this.toString()} )`
  }

  has(key: tyv.Value): boolean {
    return this.namedValues.has(key)
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
