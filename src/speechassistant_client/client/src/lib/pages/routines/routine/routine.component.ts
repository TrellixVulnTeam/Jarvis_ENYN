import {Component, EventEmitter, Input, OnInit, Output} from "@angular/core";
import {OnCommand, Routine} from "../../../data-access/models";
import {JsonObject} from "@angular/compiler-cli/ngcc/src/packages/entry_point";

@Component({
  selector: 'routine-collapse',
  templateUrl: './routine.component.html',
  styleUrls: ['./routine.component.scss']
})
export class RoutineComponent implements OnInit {
  // @ts-ignore
  @Input() routine: Routine;
  // @ts-ignore
  @Input() editName: boolean;
  clockTimes: Date[] = [];
  onCommands: OnCommand[] = [];

  @Output() private onAddOnCommandEvent: EventEmitter<any> = new EventEmitter<any>();
  @Output() private onOnCommandDeleteEvent: EventEmitter<string> = new EventEmitter<string>();
  @Output() private onRepeatDayChangeEvent: EventEmitter<[string, boolean]> = new EventEmitter<[string, boolean]>();
  @Output() private onAddClockTimeEvent: EventEmitter<any> = new EventEmitter<any>();

  ngOnInit(): void {
    /*
    for (let i = 0; i < this.routine.clock_time.length; i++) {
      let time = this.routine.clock_time[i];
      let newDate = new Date();
      newDate.setHours(<number>time["hour"]);
      newDate.setMinutes(<number>time["minute"]);
      this.clockTimes.push(newDate);
    }
     */
    for (let i = 0; i < this.routine.onCommands.length; i++) {
      this.onCommands.push(new OnCommand(i, this.routine.onCommands[i]));
    }
  }

  onAddOnCommand(): void {
    let id: number = this.onCommands.length;
    this.onCommands.push(new OnCommand(id, ""))
    this.onAddOnCommandEvent.emit();
  }

  onOnCommandDelete(id: number): void {
    const index = this.onCommands.findIndex(
      (item: OnCommand) => item.getID() === id
    )
    this.onCommands.splice(index, 1);
  }

  onRepeatDayChange(day: string, value: boolean): void {
    if (day == "monday") this.routine.monday = value;
    else if (day == "tuesday") this.routine.tuesday = value;
    else if (day == "wednesday") this.routine.wednesday = value;
    else if (day == "thursday") this.routine.thursday = value;
    else if (day == "friday") this.routine.friday = value;
    else if (day == "saturday") this.routine.saturday = value;
    else if (day == "sunday") this.routine.sunday = value;

    this.onRepeatDayChangeEvent.emit([day, value]);
  }

  onAddClockTime(): void {
    //this.routine.clock_time.push({"hour": 0, "minute": 0});
    let newDate: Date = new Date();
    newDate.setHours(0);
    newDate.setMinutes(0);
    this.clockTimes.push(newDate);
  }

  onAfterChange(event: string, value: any): void {
    if (event == "alarm") this.routine.after_alarm = value;
    if (event == "sunrise") this.routine.after_sunrise = value;
    if (event == "sunset") this.routine.after_sunset = value;
    if (event == "call") this.routine.after_call = value;
  }

  onTimeChange(time: Date, event: Date): void {
    const index = this.routine["clock_time"].findIndex(
      (item: Date) => (time.getHours() == item.getHours() && time.getMinutes() == item.getMinutes())
    )
    //this.routine["clock_time"][index] = {"hour": event.getHours(), "minute": event.getMinutes()};
    this.clockTimes[index] = event;
  }

  onTimeDelete(event: Date): void {
    const index = this.routine["clock_time"].findIndex(
      (item: Date) => (event.getHours() == item.getHours() && event.getMinutes() == item.getMinutes())
    )
    this.routine["clock_time"].splice(index, 1);
    this.clockTimes.splice(index, 1);
  }

  getDateObject(time: JsonObject): Date {
    return new Date(0, 0, 0, Number(time['hour']), Number(time['minute']));
  }
}
