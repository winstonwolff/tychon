import { JSON } from "assemblyscript-json/assembly"
import { TyValue, TyString, TyNumber, TyList } from "./TyValue"

describe('TyValue.ts', ():void => {

  test('1==2', ():void => {
    expect(1).toStrictEqual(1)
  })

  describe('TyString', ():void => {
    test('toString() returns bare string e.g. "abc"', ():void => {
      expect(new TyString('blah').toString()).toStrictEqual('blah')
    })

    test('inspect() returns string with quotes e.g. \'"abc"\'', ():void => {
      expect(new TyString('blah').inspect()).toStrictEqual('TyString("blah")')
    })
  })


  describe('TyNumber', ():void => {
    test('constructor()', ():void => {
      expect(new TyNumber(345).toString()).toStrictEqual('345.0')
    })
  })


  describe('TyList', ():void => {
    describe('get()', ():void => {
      test('returns value at given index', ():void => {
        const list = new TyList([new TyString('A')])
        expect(list.get(0)).toStrictEqual(new TyString('A'))
      })
    })

    describe('tyGet()', ():void => {
      test('returns value at given index', ():void => {
        const list = new TyList([new TyString('A')])
        expect(list.tyGet(new TyList([new TyNumber(0)]))).toStrictEqual(new TyString('A'))
      })
    })

    describe('append()', ():void => {
      test('adds element to the end', ():void => {
        const list = new TyList([new TyString('A')])
        list.append(new TyString('B'))
        expect(list).toStrictEqual(new TyList([new TyString('A'), new TyString('B')]))
      })
    })

    describe('any()', ():void => {
      const is_negative = function (x: TyValue, i:i32, s: Array<TyValue>): boolean { return x.nativeInteger() < 0 }

      test('returns True when any element evaluates to True', ():void => {
        const list = new TyList([
          new TyNumber(3),
          new TyNumber(-2),
          new TyNumber(5),
        ])
        expect(list.any(is_negative)).toStrictEqual(true)
      })
      test('returns False when no elements evaluates to True', ():void => {
        const list = new TyList([
          new TyNumber(3),
          new TyNumber(4),
          new TyNumber(5),
        ])
        // function is_negative(x: TyValue) { return x.nativeInteger() < 0 }
        expect(list.any(is_negative)).toStrictEqual(false)
      })
    })
  })


  describe('fromJsonValue()', ():void => {
    test('converts from JSON.Nums', ():void => {
      const jsonValue:JSON.Value = JSON.Value.Number(11)
      expect(TyValue.fromJsonValue(jsonValue).toString()).toStrictEqual('11.0')
    })

    test('converts from JSON.Strings', ():void => {
      const jsonValue:JSON.Value = new JSON.Str('abc')
      expect(TyValue.fromJsonValue(jsonValue).inspect()).toStrictEqual('TyString("abc")')
    })

    test('converts from JSON.Bools', ():void => {
      const jsonValue:JSON.Value = new JSON.Bool(true)
      expect(TyValue.fromJsonValue(jsonValue).inspect()).toStrictEqual('TyBoolean(true)')
    })

    test("converts JSON.Arr's to TyList's", ():void => {
      const array: JSON.Arr = JSON.Value.Array()
      array.push(new JSON.Num(123))
      array.push(new JSON.Str('abc'))
      expect(TyValue.fromJsonValue(array).inspect()).toStrictEqual('TyList(TyNumber(123.0) TyString("abc"))')
    })
  })


  describe('parseJSON()', ():void => {
    test('can parse lists', ():void => {
      expect(TyValue.parseJSON('["abc"]').inspect()).toStrictEqual('TyList(TyString("abc"))')
    })

    test('can parse list of 2', ():void => {
      expect(TyValue.parseJSON('["abc", "def"]').inspect()).toStrictEqual('TyList(TyString("abc") TyString("def"))')
    })

    test('can parse list of 3', ():void => {
      expect(TyValue.parseJSON('["abc", 123.0, "def"]').inspect()).toStrictEqual('TyList(TyString("abc") TyNumber(123.0) TyString("def"))')
    })
  })
})
