import { JSON } from "assemblyscript-json/assembly"
import { Dictionary } from "./Dictionary"
import { ArgumentList } from "./TyValue"
import * as tyv from './TyValue'


describe('Dictionary', ():void => {

  describe('new()', ():void => {
    test('returns dictionary initialized with AS Array of [key values]', ():void => {
      const d = Dictionary.new([
        [tyv.String.new('a'), tyv.String.new('AA')],
        [tyv.String.new('b'), tyv.String.new('BB')],
      ])
      expect(d.get(tyv.String.new('a'))).toStrictEqual(tyv.String.new('AA'))
      expect(d.get(tyv.String.new('b'))).toStrictEqual(tyv.String.new('BB'))
    })
  })

  describe('toString()', ():void => {

    xtest('returns a string describing the contents', ():void => {
      const d = new Dictionary()
      d.set(new tyv.String('A'), new tyv.String("FOO FOO"))
      expect(d.toString()).toStrictEqual('{"A": "FOO FOO"}')
    })
  })


  describe('inspect()', ():void => {})
    xtest('returns a string describing the contents for a programmer', ():void => {
      const d = new Dictionary()
      d.set(new tyv.String('A'), new tyv.String("FOO FOO"))
      expect(d.toString()).toStrictEqual('Dictionary( {"A": "FOO FOO"} )')
    })


  // describe('nativeDictionary()', ():void => {})


  describe('set() and get()', ():void => {
    test('returns the value that was set', ():void => {
      const d = new Dictionary()
      d.set(new tyv.String('A'), new tyv.String("FOO FOO"))

      expect(d.get(new tyv.String("A"))).toStrictEqual(new tyv.String('FOO FOO'))
    })

    // test('raises an exception when the value is not found', ():void => {
    //   const d = new Dictionary()
    //   d.set([new String("A"), new String("FOO FOO")])

    //   d.get([ new String("B") ])
    //   expect('expect an exception').toStrictEqual('to be raised') // Fail if we don't raise exception
    // })
  })

  describe('tySet() and tyGet()', ():void => {
    test('takes Tychon arguments', ():void => {
      const d = new Dictionary()
      d.tySet(ArgumentList.new([new tyv.String('A'), new tyv.String("FOO FOO")]))

      expect(d.tyGet(ArgumentList.new([ new tyv.String("A") ])))
        .toStrictEqual(new tyv.String('FOO FOO'))
    })
  })

  describe('has()', ():void => {
    test('returns True when key is in the dictionary', ():void => {
        const d = Dictionary.new([
          [tyv.String.new('rope'), tyv.String.new('ROPE')],
        ])
      // expect(d.has(tyv.String.new('rope'))).toStrictEqual(true)
    })
  })
})
