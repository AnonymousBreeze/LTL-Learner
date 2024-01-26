import { E_MODEL, E_PROMPT_TYPE } from "./converConfiguration";

export enum E_LOCAL_KEY {
    NATURAL_HISTORY = "NATURAL_HISTORY",
    CONVERT_CONFIGURATION = "CONVERT_CONFIGURATION"
}

export type I_CONVERT_HISTORY = {
    date: string;
    source: string;
    result: string;
}
export type I_CONVERT_CONFIGURATION = {
    model: E_MODEL;
    promptType: E_PROMPT_TYPE;
    temperature: number;
}