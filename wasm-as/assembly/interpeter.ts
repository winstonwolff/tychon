import { JSON } from "assemblyscript-json/assembly"

export function evaluate(code: string): i32 {
  console.log('evaluate called')
  console.log(`string="${code}"`)
  // let jsonObj: JSON.Obj = <JSON.Obj>(JSON.parse(code));
  // console.log('isArray = ', jsonObj.isArray() )

  return 30;
}
