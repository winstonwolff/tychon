import { ArgumentList } from "./TyValue"
import { ArgumentDescription } from "./ArgumentDescription"
import * as tyv from "./TyValue"

describe('ArgumentDescription', ():void => {

  describe('ofArray()', ():void => {
    test('takes convenient AS lists of strings', ():void => {
      const ad1 = ArgumentDescription.ofArray([['key', 'String'], ['value', 'String']])
      const ad2 = ArgumentDescription.new(ArgumentList.new([
        tyv.List.new([tyv.String.new("key"), tyv.String.new("String")]),
        tyv.List.new([tyv.String.new("value"), tyv.String.new("String")])
      ]))
      expect(ad1 as ArgumentDescription).toStrictEqual(ad2 as ArgumentDescription)
    })
  })

  describe('throw_if_invalid()', ():void => {
    const subject = ():ArgumentDescription => (new ArgumentDescription(ArgumentList.new([
      tyv.List.new([tyv.String.new("key"), tyv.String.new("String")]),
      tyv.List.new([tyv.String.new("value"), tyv.String.new("String")])
    ])))

    test('returns <self> when args match ArgumentDescription', ():void => {
      const arg_desc = subject()
      expect(
        arg_desc.throw_if_invalid(ArgumentList.new([
          tyv.String.new('first value'),
          tyv.String.new('second value')
        ]))
      ).toBe(arg_desc)
    })

    test('raises an error when args are incorrect type', ():void => {
      expect( () => {
        const arg_desc = subject()
        arg_desc.throw_if_invalid(ArgumentList.new([
          tyv.String.new('first value'),
          tyv.Number.new(99)
        ]))
      }).toThrow()
    })
  })
})
