import { Dictionary } from "./Dictionary.ts"
import * as tyv from "./TyValue"
import { ArgumentList, TychonFunction, TychonMacro } from "./constants"
import { zip, define } from "./builtins"

describe('bulitins.ts', ():void => {

  describe('zip()', ():void => {
    test('returns two lists combined', ():void => {
      const a = tyv.List.new([
        tyv.Number.new(1),
        tyv.Number.new(2),
        tyv.Number.new(3)])
      const b = new tyv.List([
        new tyv.TyString("apple"),
        new tyv.TyString("banana"),
        new tyv.TyString("cantelope")])

      expect(zip(null, a, b)).toStrictEqual(new tyv.List([
        new tyv.List([ tyv.Number.new(1), new tyv.TyString("apple") ]),
        new tyv.List([ tyv.Number.new(2), new tyv.TyString("banana") ]),
        new tyv.List([ tyv.Number.new(3), new tyv.TyString("cantelope") ]),
      ]))

    })
  })
  describe('define()', ():void => {
    it('saves a value in "scope"', ():void => {
      const scope = new Dictionary()
      define(scope, new tyv.List([new tyv.TyString("my_var"), new tyv.TyString("Teapot")]))

      expect(scope.get(new tyv.TyString('my_var'))).toStrictEqual(new tyv.TyString("Teapot"))
    })

    it('returns the value', ():void => {
      const scope = new Dictionary()
      const result = define(scope, new tyv.List([new tyv.TyString("my_var"), new tyv.TyString("Teapot")]))

      expect(result).toStrictEqual(new tyv.TyString("Teapot"))
    })
  })
})

