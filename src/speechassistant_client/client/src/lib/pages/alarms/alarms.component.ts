import {Component, Input, OnInit, TemplateRef} from "@angular/core";
import {Alarm} from "../../data-access/models/alarm";
import {JsonObject} from "@angular/compiler-cli/ngcc/src/packages/entry_point";
import {BackendService} from "../../data-access/service/backend.service";
import { ActivatedRoute } from "@angular/router";
import {Title} from "@angular/platform-browser";
import {BsModalRef, BsModalService} from "ngx-bootstrap/modal";

@Component({
  selector: 'alarms',
  templateUrl: './alarms.component.html',
  styleUrls: ['./alarms.component.scss']
})
export class AlarmsComponent implements OnInit{

  alarms: Alarm[];
  editMode: boolean = false;
  modalRef?: BsModalRef;
  tempAlarm: Alarm = new Alarm({}, true, true, false, true, true, false, false, false, "Guten Morgen!", "standard.wav", true);

  constructor(private route: ActivatedRoute,
              private backendService: BackendService,
              private titleService: Title,
              private modalService: BsModalService) {
  }

  ngOnInit() {
    this.titleService.setTitle('Wecker Übersicht');
    this.backendService.loadAlarms().subscribe(alarms => this.alarms = alarms);
  }

  onAddAlarm(template: TemplateRef<any>): void {
    this.tempAlarm = new Alarm({}, false, false, false, false, false, false, false, false, "Guten Morgen!", "standard.wav", true);
    this.modalRef = this.modalService.show(template);
  }

  onSaveNewAlarm(): void {
    this.alarms.push(this.tempAlarm);
    this.backendService.createAlarm(this.tempAlarm).subscribe(resultSet => {
      this.tempAlarm.id = resultSet.id;
      this.tempAlarm.text = resultSet.text; // in case that the input was malicious
    });
  }

  onDeleteAlarm(id: number): void {
    let index: number = this.alarms.findIndex(item => item.id === id);
    this.alarms.splice(index, 1);
    this.backendService.deleteAlarm(id).subscribe();
  }

  onChangeAlarm(alarm: JsonObject): void {
    let index: number = this.alarms.findIndex(item => item.id === alarm["id"]);
  }

  onChangeActivationAlarm(id: number, active: boolean): void {
    this.backendService.updateAlarmActiveState(id, active);
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
      repeatString += "jeden ";
      if (alarm.monday && alarm.tuesday && alarm.wednesday && alarm.thursday && alarm.friday) {
        if (alarm.saturday && alarm.sunday) {
          repeatString += "Tag";
        } else if (!alarm.saturday && !alarm.sunday) {
          repeatString += "Wochentag";
        }
      }
      return repeatString;
    }

    if (alarm.monday) {
    repeatString += "Montag, ";
    } if (alarm.tuesday) {
      repeatString += "Dienstag, ";
    } if (alarm.wednesday) {
      repeatString += "Mittwoch, ";
    } if (alarm.thursday) {
      repeatString += "Donnerstag, ";
    } if (alarm.friday) {
      repeatString += "Freitag, ";
    } if (alarm.saturday) {
      repeatString += "Samstag, ";
    } if (alarm.sunday) {
      repeatString += "Sonntag, ";
    }
    return this.rtrim(repeatString, ", ");
  }

  changeEditMode(): void {
    this.editMode = !this.editMode;
  }

  getEditButtonText(): string {
    return this.editMode ? "Fertig" : "Bearbeiten";
  }

  openModal(template: TemplateRef<any>) {
    this.modalRef = this.modalService.show(template);
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
