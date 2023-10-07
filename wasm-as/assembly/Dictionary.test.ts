import { JSON } from "assemblyscript-json/assembly"
import { Dictionary } from "./Dictionary"
import { ArgumentList } from "./constants"
import { TyString, TyNumber, TyList } from './TyValue'


function argList(args: Array<string>): ArgumentList {
  const jsonArr = (<JSON.Arr>JSON.from(['a', 'foo foo']))
  return jsonArr.valueOf()
}

describe('Dictionary', ():void => {
  describe('set() and get()', ():void => {
    test('returns the value that was set', ():void => {
      const d = new Dictionary()
      d.set(new TyString('A'), new TyString("FOO FOO"))

      expect(d.get(new TyString("A"))).toStrictEqual(new TyString('FOO FOO'))
    })

    // test('raises an exception when the value is not found', ():void => {
    //   const d = new Dictionary()
    //   d.set([new TyString("A"), new TyString("FOO FOO")])

    //   d.get([ new TyString("B") ])
    //   expect('expect an exception').toStrictEqual('to be raised') // Fail if we don't raise exception
    // })
  })

  describe('tySet() and tyGet()', ():void => {
    test('takes Tychon arguments', ():void => {
      const d = new Dictionary()
      d.tySet(new TyList([new TyString('A'), new TyString("FOO FOO")]))

      expect(d.tyGet(new TyList([ new TyString("A") ])))
        .toStrictEqual(new TyString('FOO FOO'))
    })
  })
})
