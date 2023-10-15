import { ArgumentDescription } from "./ArgumentDescription"
import { tyNumber, tyList, tyString } from "./TyValue"

describe('ArgumentDescription', ():void => {

  describe('throw_if_invalid()', ():void => {
    const subject = ():ArgumentDescription => (new ArgumentDescription(tyList([
      tyList([tyString("key"), tyString("TyString")]),
      tyList([tyString("value"), tyString("TyString")])
    ])))

    test('returns False when args dont match ArgumentDescription', ():void => {
      const arg_desc = subject()
      expect(
        arg_desc.throw_if_invalid(tyList([
          tyString('first value'),
          tyString('second value')
        ]))
      ).toBe(arg_desc)
    })

    test('raises an error when args don\'t match', ():void => {
      expect( () => {
        const arg_desc = subject()
        arg_desc.throw_if_invalid(tyList([
          tyString('first value'),
          tyNumber(99)
        ]))
      }).toThrow()
    })
  })

  // it raises an error when return value doesn't match type
  // it raises an error when number of args don't match
})
