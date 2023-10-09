import { ArgumentDescription } from "./ArgumentDescription"
import { TyValue, TyNumber, TyList, TyString } from "./TyValue"

describe('ArgumentDescription', ():void => {

  describe('throw_if_invalid()', ():void => {
    const subject = ():ArgumentDescription => (new ArgumentDescription(new TyList([
      new TyList([
        new TyList([new TyString("key"), new TyString("TyString")]),
        new TyList([new TyString("value"), new TyString("TyString")])
      ])
    ])))

    test('returns False when args dont match ArgumentDescription', ():void => {
      const arg_desc = subject()
      expect(
        arg_desc.throw_if_invalid(new TyList([
          new TyString('first value'),
          new TyString('second value')
        ]))
      ).toBe(arg_desc)
    })

    test('raises an error when args don\'t match', ():void => {
      expect( () => {
        const arg_desc = subject()
        arg_desc.throw_if_invalid(new TyList([
          new TyString('first value'),
          new TyNumber(99)
        ]))
      }).toThrow()
    })
  })

  // it raises an error when return value doesn't match type
  // it raises an error when number of args don't match
})
