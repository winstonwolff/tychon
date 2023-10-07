import { Dictionary } from "./Dictionary.ts"
describe('bulitins.ts', ():void => {

  describe('call()', ():void => {

    test('works with AssemblyScript functions', ():void => {
      const scope = new Dictionary()
      // expect(
      //   call(scope, TyList( TyString('Math.imul'), TyInteger(3), TyInteger(4) ))
      // ).equals(TyInteger(12) ).toBe(true)
    })

    test('works with Tychon functions', ():void => {
      const scope = new Dictionary()
      // expect(
      //   call(scope, TyList( TyString('add'), TyInteger(3), TyInteger(4) ))
      // ).equals(TyInteger(7) ).toBe(true)
    })
  })
})

