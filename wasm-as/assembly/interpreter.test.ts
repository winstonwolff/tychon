import { evaluate } from './interpreter'

describe('interpreter.ts', ():void => {
  describe('evaluate()', ():void => {

    test('can [print "hello" "world"]', ():void => {
      const code = `["print", "hello", "world"]`
      expect(evaluate(code)).toStrictEqual('TyString(\"[hello world]\")')
    })

    test('evaluates [module]', ():void => {
      const code = `["module",
          ["print", "hello", "world"],
          ["print", "I'm", "a", "Module"],
        ]`
      expect(evaluate(code)).toStrictEqual(`TyList(TyString("[hello world]") TyString("[I'm a Module]"))`)
    })

    test('can define variable', ():void => {
      const code = `["module",
          ["print", "hello", "world"],
          ["print", "I'm", "a", "Module"],
        ]`
      expect(evaluate(code)).toStrictEqual(`TyList(TyString("[hello world]") TyString("[I'm a Module]"))`)
    })
  })
})

