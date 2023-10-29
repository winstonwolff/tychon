// Shared constants and types

import * as tyv from './TyValue'
import { Dictionary } from "./Dictionary"

export type ArgumentList = tyv.List
export type TychonFunction = (args:ArgumentList) => tyv.Value
export type TychonMacro = (scope: Dictionary, args:ArgumentList) => tyv.Value


