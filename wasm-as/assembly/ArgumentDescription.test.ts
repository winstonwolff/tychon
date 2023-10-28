import { ArgumentDescription } from "./ArgumentDescription"
import * as tyv from "./TyValue"

describe('ArgumentDescription', ():void => {

  describe('throw_if_invalid()', ():void => {
    const subject = ():ArgumentDescription => (new ArgumentDescription(tyv.List.new([
      tyv.List.new([tyv.TyString.new("key"), tyv.TyString.new("TyString")]),
      tyv.List.new([tyv.TyString.new("value"), tyv.TyString.new("TyString")])
    ])))

    test('returns False when args dont match ArgumentDescription', ():void => {
      const arg_desc = subject()
      expect(
        arg_desc.throw_if_invalid(tyv.List.new([
          tyv.TyString.new('first value'),
          tyv.TyString.new('second value')
        ]))
      ).toBe(arg_desc)
    })

    test('raises an error when args don\'t match', ():void => {
      expect( () => {
        const arg_desc = subject()
        arg_desc.throw_if_invalid(tyv.List.new([
          tyv.TyString.new('first value'),
          tyv.Number.new(99)
        ]))
      }).toThrow()
    })
  })

  // it raises an error when return value doesn't match type
  // it raises an error when number of args don't match
})
