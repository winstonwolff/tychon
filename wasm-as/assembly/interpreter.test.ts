import { evaluateJson } from './interpreter'
import { ArgumentList, TychonMacro } from "./constants.ts"
import { Dictionary } from "./Dictionary.ts"
import { TyValue, TyList, TyNumber, TyString } from "./TyValue"
import * as builtins from "./builtins.ts"

describe('interpreter.ts', ():void => {
  describe('evaluateJson()', ():void => {

    test('can [print "hello" "world"]', ():void => {
      const code = `["print", "hello", "world"]`
      expect(evaluateJson(code)).toStrictEqual('TyString(\"hello world\")')
    })

    test('evaluates [module]', ():void => {
      const code = `["module",
          ["print", "hello", "world"],
          ["print", "I'm", "a", "Module"],
        ]`
      expect(evaluateJson(code)).toStrictEqual(`TyList(TyString("hello world") TyString("I'm a Module"))`)
    })

    test('can define variable', ():void => {
      const code = `["module",
          ["define", "name", "winston"],
          ["print", "hello", ["symbol", "name"]],
        ]`
      expect(evaluateJson(code)).toStrictEqual(`TyList(TyString("winston") TyString("hello winston"))`)
    })
  })

  describe('symbol()', ():void => {
    const double = (args: ArgumentList): TyValue => {
      return new TyNumber(args.get(0).nativeInteger() * 2 )
    }

    it('fetches the value in scope', ():void => {
      const scope = new Dictionary()
      builtins.define(scope, new TyList([new TyString("my_var"), new TyString("Teapot")]))

      expect<TyValue>(builtins.symbol(scope, new TyList([new TyString("my_var")]))).toStrictEqual(new TyString("Teapot"))
    })

    xit('fetches functions too', ():void => {
      const scope = new Dictionary()
      // const tyDouble = new TyASFunction(double, 'double')
      // define(scope, new TyList([new TyString("double"), tyDouble]))
      // expect(new_lookup(scope, new TyList([new TyString("double")]))).toStrictEqual(tyDouble)
    })
  })
})

