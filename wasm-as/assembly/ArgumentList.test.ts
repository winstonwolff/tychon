import { ArgumentDescription } from "./ArgumentList"
import { TyValue, TyNumber, TyList, TyString } from "./TyValue"

describe('ArgumentDescription', ():void => {

  describe('is_valid()', ():void => {
    test('returns False when args dont match ArgumentDescription', ():void => {
      const arg_desc = new ArgumentDescription(new TyList([
        new TyList([new TyString("key"), new TyString("TyString")]),
        new TyList([new TyString("value"), new TyString("TyString")])
      ]))
      expect(
        arg_desc.is_valid(new TyList([
          new TyString('first value'),
          new TyString('second value')
        ]))
      ).toBe(true)

      expect(
        arg_desc.is_valid(new TyList([
          new TyString('first value'),
          new TyNumber(99)
        ]))
      ).toBe(false)
    })
  })

    // test('it raises an error when parameters dont match types'
    // it raises an error when return value doesn't match type
    // it raises an error when number of args don't match
})
