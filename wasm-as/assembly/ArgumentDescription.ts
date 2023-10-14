import { TyValue, TyString, TyList, TyFalse } from "./TyValue"
import { ArgumentList } from "./constants.ts"
import { zip } from "./builtins"

/*
  Parameter — the variable in the declaration of the function. 
  Argument — the actual value of this variable that gets passed to the function.
  Mnenomic: parameter -> placeholder;  argument -> actual value

*/
export const tyArgumentDescription = (parameter_names_and_types: TyList):ArgumentDescription =>
  ( new ArgumentDescription(parameter_names_and_types) )

export class ArgumentDescription extends TyValue {
  parameter_names_and_types: TyList

  constructor(args: ArgumentList) {
    super()
    this.parameter_names_and_types = args.get(0) as TyList
  }

  toString(): string {
    return this.inspect()
  }

  inspect(): string {
    return `ArgumentDescription(${this.parameter_names_and_types.inspect()})`
  }

  throw_if_invalid(args: ArgumentList): ArgumentDescription {
    if (this.parameter_names_and_types.length() != args.length()) {
      throw new Error(`ArgumentDescription: ${args.length()} args provided for args: ${this}`)
    }

    const params_and_args = zip(null, this.parameter_names_and_types, args)
    params_and_args.tyMap( (args: ArgumentList):TyValue => {
      // input:
      const param_and_arg:TyList = (args as TyList).get(0) as TyList

      const param_pair: TyList = param_and_arg.get(0) as TyList
      const param_name = param_pair.get(0)
      const param_type_str = param_pair.get(1)
      const arg = (param_and_arg as TyList).get(1)

      if (param_type_str.nativeString() != arg.type_name) {
        throw new Error(`Parameter '${param_name}' must be a ${param_type_str.nativeString()} but was ${arg.inspect()}`)
      }
      return TyFalse
    })

    return this
  }
}
