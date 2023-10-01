// Shared constants and types

import { TyValue, TyString, TyNumber } from './TyValue'
import { JSON } from "assemblyscript-json/assembly"

export type List = Array<JSON.Value>
export type ArgumentList = Array<TyValue>
export type TychonFunction = (args:ArgumentList) => TyValue


