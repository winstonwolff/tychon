import { JSON } from "assemblyscript-json/assembly"
import * as tyv from "./TyValue"
import { ArgumentList } from "./TyValue"
import { ArgumentDescription } from "./ArgumentDescription"
import { Dictionary } from "./Dictionary"
import { TychonFunction, TychonMacro } from "./constants"

describe('TyValue.ts', ():void => {


  describe('Value', ():void => {

    describe('fromJsonValue()', ():void => {
      test('converts from JSON.Nums', ():void => {
        const jsonValue:JSON.Value = JSON.Value.Number(11)
        expect(tyv.Value.fromJsonValue(jsonValue).toString()).toStrictEqual('11.0')
      })

      test('converts from JSON.Strings', ():void => {
        const jsonValue:JSON.Value = new JSON.Str('abc')
        expect(tyv.Value.fromJsonValue(jsonValue).inspect()).toStrictEqual('String("abc")')
      })

      test('converts from JSON.Bools', ():void => {
        const jsonValue:JSON.Value = new JSON.Bool(true)
        expect(tyv.Value.fromJsonValue(jsonValue).inspect()).toStrictEqual('Boolean(true)')
      })

      test("converts JSON.Arr's to List's", ():void => {
        const array: JSON.Arr = JSON.Value.Array()
        array.push(new JSON.Num(123))
        array.push(new JSON.Str('abc'))
        expect(tyv.Value.fromJsonValue(array).inspect()).toStrictEqual('List(Number(123.0) String("abc"))')
      })
    })


    describe('parseJSON()', ():void => {
      test('can parse lists', ():void => {
        expect(tyv.Value.parseJSON('["abc"]').inspect()).toStrictEqual('List(String("abc"))')
      })

      test('can parse list of 2', ():void => {
        expect(tyv.Value.parseJSON('["abc", "def"]').inspect()).toStrictEqual('List(String("abc") String("def"))')
      })

      test('can parse list of 3', ():void => {
        expect(tyv.Value.parseJSON('["abc", 123.0, "def"]').inspect()).toStrictEqual('List(String("abc") Number(123.0) String("def"))')
      })
    })
  })


  describe('String', ():void => {
    test('toString() returns bare string e.g. "abc"', ():void => {
      expect(new tyv.String('blah').toString()).toStrictEqual('blah')
    })

    test('inspect() returns string with quotes e.g. \'"abc"\'', ():void => {
      expect(new tyv.String('blah').inspect()).toStrictEqual('String("blah")')
    })
  })


  describe('Number', ():void => {
    test('constructor()', ():void => {
      expect(tyv.Number.new(345).toString()).toStrictEqual('345.0')
    })
  })


  describe('List', ():void => {
    describe('get()', ():void => {
      test('returns value at given index', ():void => {
        const list = new tyv.List([new tyv.String('A')])
        expect(list.get(0)).toStrictEqual(new tyv.String('A'))
      })
    })

    describe('tyGet()', ():void => {
      test('returns value at given index', ():void => {
        const list = new tyv.List([new tyv.String('A')])
        expect(list.tyGet(ArgumentList.new([tyv.Number.new(0)]))).toStrictEqual(new tyv.String('A'))
      })
    })

    describe('append()', ():void => {
      test('adds element to the end', ():void => {
        const list = new tyv.List([new tyv.String('A')])
        list.append(new tyv.String('B'))
        expect(list).toStrictEqual(new tyv.List([new tyv.String('A'), new tyv.String('B')]))
      })
    })

    describe('map()', ():void => {
      test('returns new Array with results of callback(v)', ():void => {
        const list = new tyv.List([
          tyv.Number.new(3),
          tyv.Number.new(-2),
          tyv.Number.new(5),
        ])
        const f = (v: tyv.Value, index:i32, self:Array<tyv.Value>):tyv.Value => {
          return tyv.Number.new(v.nativeInteger() * 2)
        }

        expect(list.map(f)).toStrictEqual([
          tyv.Number.new(6),
          tyv.Number.new(-4),
          tyv.Number.new(10),
        ])
      })
    })

    describe('tyMap()', ():void => {
      test('returns new List with results of callback(v)', ():void => {
        const list = new tyv.List([
          tyv.Number.new(3),
          tyv.Number.new(-2),
          tyv.Number.new(5),
        ])
        const f = (args: ArgumentList):tyv.Value => {
          const v = args.get(0)
          return tyv.Number.new(v.nativeInteger() * 2)
        }

        expect(list.tyMap(f)).toStrictEqual(new tyv.List([
          tyv.Number.new(6),
          tyv.Number.new(-4),
          tyv.Number.new(10),
        ]))
      })
    })

    describe('any()', ():void => {
      const is_negative = function (x: tyv.Value, i:i32, s: Array<tyv.Value>): boolean { return x.nativeInteger() < 0 }

      test('returns True when any element evaluates to True', ():void => {
        const list = new tyv.List([
          tyv.Number.new(3),
          tyv.Number.new(-2),
          tyv.Number.new(5),
        ])
        expect(list.any(is_negative)).toStrictEqual(true)
      })
      test('returns False when no elements evaluates to True', ():void => {
        const list = new tyv.List([
          tyv.Number.new(3),
          tyv.Number.new(4),
          tyv.Number.new(5),
        ])
        // function is_negative(x: TyValue) { return x.nativeInteger() < 0 }
        expect(list.any(is_negative)).toStrictEqual(false)
      })
    })
  })


  describe('ArgumentList', ():void => {
    describe('ofList()', ():void => {
      test('takes List of args', ():void => {
        const l = tyv.ArgumentList.ofList(tyv.List.new([tyv.String.new('R')]))
        const a = tyv.ArgumentList.new([tyv.String.new('R')])
        expect(l).toStrictEqual(a)
      })
    })
  })

  describe('Macro', ():void => {
    test('executes Tychon code', ():void => {
      const m:tyv.Macro = tyv.Macro.new(
        'foo',
        ArgumentDescription.ofArray([]),
        tyv.String.new("FOO")
      )
      const scope = new Dictionary()
      expect<tyv.Value>(m.__call__(scope, ArgumentList.new([]))).toStrictEqual(tyv.String.new("FOO"))
    })
  })

  describe('NativeMacro', ():void => {
    test('executes an AssemblyScript function', ():void => {
      const m = new tyv.NativeMacro(
        'foo',
        ArgumentDescription.ofArray([]),
        function foo(scope: Dictionary, args: ArgumentList):tyv.Value { return new tyv.String("FOO") }
      )
      const scope = new Dictionary()
      expect<tyv.Value>(m.__call__(scope, ArgumentList.new([]))).toStrictEqual(tyv.String.new("FOO"))
    })
  })
})
