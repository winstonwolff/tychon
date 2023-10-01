// Shared constants and types

import { JSON } from "assemblyscript-json/assembly"

export type List = Array<JSON.Value>
export type ArgumentList = Array<JSON.Value>
export type TychonFunction = (args:ArgumentList) => JSON.Value


