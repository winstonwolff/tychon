// Shared constants and types

import { TyValue, TyString, TyNumber, TyList } from './TyValue'
import { JSON } from "assemblyscript-json/assembly"
import { Dictionary } from "./Dictionary"

export type ArgumentList = TyList
export type TychonFunction = (args:ArgumentList) => TyValue
export type TychonMacro = (scope: Dictionary, args:ArgumentList) => TyValue


