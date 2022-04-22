
import {Component, Input, OnInit} from "@angular/core";
import {Alarm} from "../../data-access/models/alarm";
import {JsonObject} from "@angular/compiler-cli/ngcc/src/packages/entry_point";
import {throwMatDialogContentAlreadyAttachedError} from "@angular/material/dialog";
import {BackendService} from "../../data-access/service/backend.service";
import {Title} from "@angular/platform-browser";

@Component({
  selector: 'alarm',
  templateUrl: './alarm.component.html',
  styleUrls: ['./alarm.component.scss']
})
export class AlarmComponent implements OnInit{

  @Input() alarm: Alarm;

  constructor(private backendService: BackendService, private titleService: Title) {
  }

  ngOnInit() {
    this.titleService.setTitle('Wecker');
    this.alarm = new Alarm({}, true, true, false, true, true, false, false, false, "Guten Morgen!", "standard.wav", true);
  }


  onDeleteAlarm(id: number): void {
  }

  onChangeAlarm(alarm: JsonObject): void {

  }

  onChangeActivationAlarm(id: number, active: boolean): void {

  }

  getTimeString(alarm: Alarm): string {
    let time: Date = alarm.time;
    let hours: string = time.getHours().toString().padStart(2, '0');
    let minutes: string = time.getMinutes().toString().padStart(2, '0');
    return hours+":"+minutes;
  }

  getRepeatingString(alarm: Alarm): string {
    let repeatString: string = "";
    if (alarm.regular) {
      repeatString += "jeden "
    }

    if (alarm.monday && alarm.tuesday && alarm.wednesday && alarm.thursday && alarm.friday) {
      if (alarm.saturday && alarm.sunday) {
        repeatString += "Tag"
      } else if (!alarm.saturday && !alarm.sunday) {
        repeatString += "Wochentag"
      }
    } else {
      if (alarm.monday) {
      repeatString += "Montag, ";
      }
      if (alarm.tuesday) {
        repeatString += "Dienstag, ";
      }
      if (alarm.wednesday) {
        repeatString += "Mittwoch, ";
      }
      if (alarm.thursday) {
        repeatString += "Donnerstag, ";
      }
      if (alarm.friday) {
        repeatString += "Freitag, ";
      }
      if (alarm.saturday) {
        repeatString += "Samstag, ";
      }
      if (alarm.sunday) {
        repeatString += "Sonntag, ";
      }
    }
    return this.rtrim(repeatString, ", ");
  }

  rtrim(input: string, characters: string): string {
    let start = 0;
    let end = input.length - 1;
    while (characters.indexOf(input[end]) >= 0) {
      end -= 1;
    }
    return input.substr(0, end + 1);
  }
}
