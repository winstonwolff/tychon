import { evaluateJson } from './interpreter'
import { ArgumentList } from "./TyValue"
import { TychonMacro } from "./constants.ts"
import { Dictionary } from "./Dictionary.ts"
import * as tyv from "./TyValue"
import * as builtins from "./builtins.ts"

describe('interpreter.ts', ():void => {
  describe('evaluateJson()', ():void => {

    test('can [print "hello" "world"]', ():void => {
      const code = `["print", "hello", "world"]`
      expect(evaluateJson(code)).toStrictEqual('String(\"hello world\")')
    })

    test('evaluates [module]', ():void => {
      const code = `["module",
          ["print", "hello", "world"],
          ["print", "I'm", "a", "Module"],
        ]`
      expect(evaluateJson(code)).toStrictEqual(`List(String("hello world") String("I'm a Module"))`)
    })

    test('can define variable', ():void => {
      const code = `["module",
          ["define", "name", "winston"],
          ["print", "hello", ["symbol", "name"]],
        ]`
      expect(evaluateJson(code)).toStrictEqual(`List(String("winston") String("hello winston"))`)
    })
  })

  describe('symbol()', ():void => {
    const double = (args: ArgumentList): tyv.Value => {
      return tyv.Number.new(args.get(0).nativeInteger() * 2 )
    }

    it('fetches the value in scope', ():void => {
      const scope = new Dictionary()
      builtins.define(scope, ArgumentList.new([new tyv.String("my_var"), new tyv.String("Teapot")]))

      expect<tyv.Value>(builtins.symbol(scope, ArgumentList.new([new tyv.String("my_var")]))).toStrictEqual(new tyv.String("Teapot"))
    })

    xit('fetches functions too', ():void => {
      const scope = new Dictionary()
      // const tyDouble = new TyASFunction(double, 'double')
      // define(scope, new List([new String("double"), tyDouble]))
      // expect(new_lookup(scope, new List([new String("double")]))).toStrictEqual(tyDouble)
    })
  })
})

