import { ArgumentDescription } from "./ArgumentList"
import { TyValue, TyString } from "./TyValue"

describe('ArgumentDescription', ():void => {

  describe('new', ():void => {
    test('takes a list of arguments', ():void => {
      const ad = new ArgumentDescription([
        ["key", "String"],
        ["value", "String"]
      ])
    })
  })

  describe('is_valid()', ():void => {
    test('returns False when args dont match ArgumentDescription', ():void => {
      const ad = new ArgumentDescription([
        ["key", "TyString"],
        ["value", "TyString"]
      ])
      expect(
        ad.is_valid(new TyList([ new TyString('first value'), new TyString('second value')]))
      ).toBe(true)
    })
  })

    // test('it raises an error when parameters dont match types'
    // it raises an error when return value doesn't match type
    // it raises an error when number of args don't match
})
