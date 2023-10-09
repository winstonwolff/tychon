import { Dictionary } from "./Dictionary.ts"
import { TyList, TyValue, TyNumber, TyString } from "./TyValue"
import { ArgumentList, TychonFunction, TychonMacro } from "./constants"
import { zip, define, new_lookup } from "./builtins"

describe('bulitins.ts', ():void => {

  describe('zip()', ():void => {
    test('returns two lists combined', ():void => {
      const a = new TyList([
        new TyNumber(1),
        new TyNumber(2),
        new TyNumber(3)])
      const b = new TyList([
        new TyString("apple"),
        new TyString("banana"),
        new TyString("cantelope")])

      expect(zip(null, a, b)).toStrictEqual(new TyList([
        new TyList([ new TyNumber(1), new TyString("apple") ]),
        new TyList([ new TyNumber(2), new TyString("banana") ]),
        new TyList([ new TyNumber(3), new TyString("cantelope") ]),
      ]))

    })
  })
  describe('define()', ():void => {
    it('saves a value in "scope"', ():void => {
      const scope = new Dictionary()
      define(scope, new TyList([new TyString("my_var"), new TyString("Teapot")]))

      expect(scope.get(new TyString('my_var'))).toStrictEqual(new TyString("Teapot"))
    })

    it('returns the value', ():void => {
      const scope = new Dictionary()
      const result = define(scope, new TyList([new TyString("my_var"), new TyString("Teapot")]))

      expect(result).toStrictEqual(new TyString("Teapot"))
    })
  })

  describe('lookup()', ():void => {
    const double = (args: ArgumentList): TyValue => {
      return new TyNumber(args.get(0).nativeInteger() * 2 )
    }

    it('fetches the value in scope', ():void => {
      const scope = new Dictionary()
      const result = define(scope, new TyList([new TyString("my_var"), new TyString("Teapot")]))

      expect(new_lookup(scope, new TyList([new TyString("my_var")]))).toStrictEqual(new TyString("Teapot"))
    })

    it('fetches functions too', ():void => {
      const scope = new Dictionary()
      define(scope, new TyFunction([new TyString("double"), double]))
      expect(new_lookup(scope, new TyList([new TyString("double")]))).toStrictEqual(double)
    })
  })
})

