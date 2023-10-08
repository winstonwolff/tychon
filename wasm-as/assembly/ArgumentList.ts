import { TyValue, TyString, TyList } from "./TyValue"
import { ArgumentList } from "./constants.ts"
import { zip } from "./builtins"

/*
  Parameter — the variable in the declaration of the function. 
  Argument — the actual value of this variable that gets passed to the function.
  Mnenomic: parameter -> placeholder;  argument -> actual value

*/
export class ArgumentDescription extends TyValue {
  parameter_names_and_types: TyList

  constructor(parameter_names_and_types: ArgumentList) {
    super()
    this.parameter_names_and_types = parameter_names_and_types
  }

  is_valid(args: ArgumentList): boolean {
    const params_and_args = zip(null, this.parameter_names_and_types, args)
    const args_types_dont_match = params_and_args.any(
      function is_matching_type(param_and_arg: TyValue, i:i32, s:Array<TyValue>){
        const param_pair = (param_and_arg as TyList).get(0)
        const arg: TyValue = (param_and_arg as TyList).get(1)
        const param_type_str = (param_pair as TyList).get(1)

        return arg.type_name != param_type_str.nativeString()
      })

    return ! args_types_dont_match
  }
}
