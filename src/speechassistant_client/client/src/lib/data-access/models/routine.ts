import { JsonObject } from "@angular/compiler-cli/ngcc/src/packages/entry_point";

export interface Routine {
  name: string;
  description: string;
  onCommands: string[];
  monday: boolean;
  tuesday: boolean;
  wednesday: boolean;
  thursday: boolean;
  friday: boolean;
  saturday: boolean;
  sunday: boolean;
  dateOfDay: Date[];
  clock_time: Date[];
  after_alarm: boolean;
  after_sunrise: boolean;
  after_sunset: boolean;
  after_call: boolean;
  commands: JsonObject[];
}
