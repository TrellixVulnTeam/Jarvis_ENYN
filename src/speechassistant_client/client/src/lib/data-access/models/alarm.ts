import {JsonObject} from "@angular/compiler-cli/ngcc/src/packages/entry_point";

export interface Alarm {
  id?: number;
  time: JsonObject;
  timeObject?: Date;
  monday: boolean;
  tuesday: boolean;
  wednesday: boolean;
  thursday: boolean;
  friday: boolean;
  saturday: boolean;
  sunday: boolean;
  regular: boolean;
  active: boolean;
  text: string;
  sound: string;
  user: number;
  initiated: boolean;
  last_executed: string;
}


