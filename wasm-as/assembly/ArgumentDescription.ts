import * as tyv from "./TyValue"
import { ArgumentList } from "./constants.ts"
import { zip } from "./builtins"

/*
  Parameter — the variable in the declaration of the function. 
  Argument — the actual value of this variable that gets passed to the function.
  Mnenomic: parameter -> placeholder;  argument -> actual value

*/
export const tyArgumentDescription = (argDesc: tyv.List):ArgumentDescription =>
  ( new ArgumentDescription(argDesc) )

export class ArgumentDescription extends tyv.Value {
  argDesc: tyv.List

  constructor(args: ArgumentList) {
    super()
    this.argDesc = args
  }

  static new(args: ArgumentList): ArgumentDescription {
    return new ArgumentDescription(args)
  }

  toString(): string {
    return this.inspect()
  }

  inspect(): string {
    return `ArgumentDescription(${this.argDesc.inspect()})`
  }

  throw_if_invalid(args: ArgumentList): ArgumentDescription {
    if (this.argDesc.length() != args.length()) {
      throw new Error(`ArgumentDescription: ${args.length()} args provided for args: ${this}`)
    }

    const params_and_args = zip(null, this.argDesc, args)
    params_and_args.tyMap( (args: ArgumentList):tyv.Value => {
      // input:
      const param_and_arg:tyv.List = (args as tyv.List).get(0) as tyv.List

      const param_pair: tyv.List = param_and_arg.get(0) as tyv.List
      const param_name = param_pair.get(0)
      const param_type_str = param_pair.get(1)
      const arg = (param_and_arg as tyv.List).get(1)

      if (param_type_str.nativeString() != arg.type_name) {
        throw new Error(`Parameter '${param_name}' must be a ${param_type_str.nativeString()} but was ${arg.inspect()}`)
      }
      return tyv.False
    })

    return this
  }
}
