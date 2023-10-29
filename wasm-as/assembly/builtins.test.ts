import { Dictionary } from "./Dictionary.ts"
import * as tyv from "./TyValue"
import { ArgumentList } from "./TyValue"
import { TychonFunction, TychonMacro } from "./constants"
import { zip, define } from "./builtins"

describe('bulitins.ts', ():void => {

  describe('zip()', ():void => {
    test('returns two lists combined', ():void => {
      const a = tyv.List.new([
        tyv.Number.new(1),
        tyv.Number.new(2),
        tyv.Number.new(3)])
      const b = new tyv.List([
        new tyv.String("apple"),
        new tyv.String("banana"),
        new tyv.String("cantelope")])

      expect(zip(null, a, b)).toStrictEqual(new tyv.List([
        new tyv.List([ tyv.Number.new(1), new tyv.String("apple") ]),
        new tyv.List([ tyv.Number.new(2), new tyv.String("banana") ]),
        new tyv.List([ tyv.Number.new(3), new tyv.String("cantelope") ]),
      ]))

    })
  })
  describe('define()', ():void => {
    it('saves a value in "scope"', ():void => {
      const scope = new Dictionary()
      define(scope, new ArgumentList([tyv.String.new("my_var"), new tyv.String("Teapot")]))

      expect(scope.get(new tyv.String('my_var'))).toStrictEqual(new tyv.String("Teapot"))
    })

    it('returns the value', ():void => {
      const scope = new Dictionary()
      const result = define(scope, ArgumentList.new([new tyv.String("my_var"), new tyv.String("Teapot")]))

      expect(result).toStrictEqual(new tyv.String("Teapot"))
    })
  })
})

