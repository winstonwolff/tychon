import { JSON } from "assemblyscript-json/assembly"
import { ArgumentList } from "./constants.ts"
import { TyValue, TyString, TyNumber, TyList } from './TyValue'

export class Dictionary extends TyValue {
  namedValues: Map<string, TyValue>

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

  has(key: TyValue): boolean {
    return this.namedValues.has(key)
  }

  // store 'value' under 'key'
  set(key: TyValue, value: TyValue): TyValue {
    this.namedValues.set(this._normalizedKey(key), value)
    return value
  }

  // same as set(), but with Tychon args
  tySet(args: ArgumentList): TyValue {
    // inputs:
    const key = (args as TyList).get(0)
    const value = (args as TyList).get(1)

    this.set(key, value)
    return value
  }

  // Returns the value by 'key'
  get(key: TyValue): TyValue {
    return this.namedValues.get(this._normalizedKey(key))
  }

  // same as get() but with Tychon args
  tyGet(args: ArgumentList): TyValue {
    // inputs:
    const key = (args as TyList).get(0) // The key of the value you want

    return this.get(key)
  }

  _normalizedKey(k: TyValue): string {
    return k.inspect()
  }
}
