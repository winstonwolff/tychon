import { JSON } from "assemblyscript-json/assembly"
import { ArgumentList } from "./constants.ts"
import { TyValue, TyString, TyNumber } from './TyValue'

export class Dictionary {
  namedValues: Map<string, TyValue>

  constructor() {
    this.namedValues = new Map()
  }

  // associates 'value' with 'name' in the scope. It can be retrieved later.
  set(args: ArgumentList): TyValue {
    // inputs:
    const name = args[0]
    const value = args[1]

    this.namedValues.set(this._internedKey(name), value)
    return value
  }

  // Returns the value by 'name'
  get(args: ArgumentList): TyValue {
    // inputs:
    const name = args[0] // The name of the value you want

    return this.namedValues.get(this._internedKey(name))
  }

  _internedKey(k: TyValue): string {
    return k.inspect()
  }
}
