import { evaluate } from './interpreter'

describe('interpreter.ts', ():void => {
  describe('evaluate()', ():void => {
    test('can call print()', ():void => {
      const code = `["print", "hello", "world"]`
      expect(evaluate(code)).toStrictEqual('TyString(\"[hello world]\")')
    })
  })
})

