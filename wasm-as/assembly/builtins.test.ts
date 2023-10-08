import { Dictionary } from "./Dictionary.ts"
import { zip } from "./builtins"
import { TyList, TyValue, TyNumber, TyString } from "./TyValue"

describe('bulitins.ts', ():void => {

  describe('call()', ():void => {

    // test('works with AssemblyScript functions', ():void => {
    //   const scope = new Dictionary()
    //   expect(
    //     call(scope, TyList( TyString('Math.imul'), TyInteger(3), TyInteger(4) ))
    //   ).equals(TyInteger(12) ).toBe(true)
    // })

    // test('works with Tychon functions', ():void => {
    //   const scope = new Dictionary()
    //   expect(
    //     call(scope, TyList( TyString('add'), TyInteger(3), TyInteger(4) ))
    //   ).equals(TyInteger(7) ).toBe(true)
    // })
  })

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
    // it('saves a value in "scope"', ():void => {
    //   const scope = new Dictionary()
    //   expect(scope.get('my_var')).toStrictEqual(

    // })
  })


})

