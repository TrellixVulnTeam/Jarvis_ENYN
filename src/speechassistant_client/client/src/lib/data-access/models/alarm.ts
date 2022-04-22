import {JsonObject} from "@angular/compiler-cli/ngcc/src/packages/entry_point";
import {compareNumbers} from "@angular/compiler-cli/src/version_helpers";
import {runTempPackageBin} from "@angular/cli/utilities/install-package";

export class Alarm {
  id?: number;
  time: Date;
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


  constructor(time: JsonObject, monday: boolean, tuesday: boolean, wednesday: boolean, thursday: boolean, friday: boolean, saturday: boolean, sunday: boolean, regular: boolean, text: string, sound: string, active: boolean, id?: number) {
    if (id) {
      this.id = id;
    }
    this.time = new Date();
    this.time.setHours(time["hour"] as number);
    this.time.setMinutes(time["minute"] as number);
    this.monday = monday;
    this.tuesday = tuesday;
    this.wednesday = wednesday;
    this.thursday = thursday;
    this.friday = friday;
    this.saturday = saturday;
    this.sunday = sunday;
    this.regular = regular;
    this.active = active;
    this.text = text;
    this.sound = sound;
  }


}
