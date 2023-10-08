import { TyValue, TyString } from "./TyValue"

export class ArgumentDescription extends TyValue {
  constructor(namesAndTypes: Array<Array<string>>) {
    super()
  }

  is_valid(ArgumentList): boolean {
    return false
  }
}
