import {Component, OnInit, TemplateRef, ViewChild} from "@angular/core";
import {Alarm} from "../../data-access/models/alarm";
import {BackendService} from "../../data-access/service/backend.service";
import {ActivatedRoute} from "@angular/router";
import {Title} from "@angular/platform-browser";
import {BsModalRef, BsModalService} from "ngx-bootstrap/modal";
import {AlarmStore} from "../../data-access/service/store/alarm.store";

@Component({
  selector: 'alarms',
  templateUrl: './alarms.component.html',
  styleUrls: ['./alarms.component.scss']
})
export class AlarmsComponent implements OnInit {

  alarms: Alarm[] = [];
  editMode: boolean = false
  createModalRef?: BsModalRef;
  repeatingModalRef?: BsModalRef;
  textModalRef?: BsModalRef;
  // @ts-ignore
  @ViewChild('createAlarmModal') createModal: TemplateRef<any>;
  // @ts-ignore
  @ViewChild('createAlarmChangeRepeating') createRepeatModal: TemplateRef<any>;
  // @ts-ignore
  @ViewChild('createAlarmChangeText') createTextModal: TemplateRef<unknown>;
  // @ts-ignore
  tempAlarm: Alarm = {
    time: {},
    timeObject: new Date(),
    monday: false,
    tuesday: false,
    wednesday: false,
    thursday: false,
    friday: false,
    saturday: false,
    sunday: false,
    regular: false,
    active: true,
    text: "Guten Morgen!",
    sound: "standard"
  };

  constructor(private route: ActivatedRoute,
              private backendService: BackendService,
              private titleService: Title,
              private modalService: BsModalService,
              private alarmService: AlarmStore) {
  }

  ngOnInit() {
    this.titleService.setTitle('Wecker Übersicht');
    this.alarmService.getAlarms().subscribe(alarms => {
      this.alarms = alarms;
    });
  }

  onAddAlarm(template: TemplateRef<any>): void {
    this.tempAlarm = {
      time: {},
      timeObject: new Date(),
      monday: false,
      tuesday: false,
      wednesday: false,
      thursday: false,
      friday: false,
      saturday: false,
      sunday: false,
      regular: false,
      active: true,
      text: "Guten Morgen!",
      sound: "standard",
      last_executed: "",
      user: -1,
      initiated: false
    };
    // @ts-ignore
    this.tempAlarm.timeObject.setHours(12);
    // @ts-ignore
    this.tempAlarm.timeObject.setMinutes(0);
    this.createModalRef = this.modalService.show(template);
  }

  onSaveNewAlarm(): void {
    this.alarmService.addAlarm(this.tempAlarm);
    this.closeAllModals();
  }

  onDeleteAlarm(id: number): void {
    this.alarmService.deleteAlarm(id);
  }

  onChangeAlarm(alarm: Alarm): void {
    this.alarmService.updateAlarm(alarm);
  }

  onChangeActivationAlarm(id: number, active: boolean): void {
    this.alarmService.updateAlarmActiveStatus(id, active);
  }

  getTimeString(alarm: Alarm): string {
    // @ts-ignore
    let timeObject: Date = alarm.timeObject;
    let hours: string = timeObject.getHours().toString().padStart(2, '0');
    let minutes: string = timeObject.getMinutes().toString().padStart(2, '0');
    return hours + ":" + minutes;
  }

  getRepeatingString(alarm: Alarm): string {
    let repeatString: string = "";
    if (alarm.regular) {
      repeatString += "immer ";
    }

    if (alarm.monday && alarm.tuesday && alarm.wednesday && alarm.thursday && alarm.friday) {
      if (alarm.saturday && alarm.sunday) {
        repeatString += "an allen Tagen";
      } else if (!alarm.saturday && !alarm.sunday) {
        repeatString += "Wochentags";
      }
      return repeatString;
    }

    if (alarm.monday) {
      repeatString += "Montags, ";
    }
    if (alarm.tuesday) {
      repeatString += "Dienstags, ";
    }
    if (alarm.wednesday) {
      repeatString += "Mittwochs, ";
    }
    if (alarm.thursday) {
      repeatString += "Donnerstags, ";
    }
    if (alarm.friday) {
      repeatString += "Freitags, ";
    }
    if (alarm.saturday) {
      repeatString += "Samstags, ";
    }
    if (alarm.sunday) {
      repeatString += "Sonntags, ";
    }
    return this.rtrim(repeatString, ", ");
  }

  changeEditMode(): void {
    this.editMode = !this.editMode;
  }

  getEditButtonText(): string {
    return this.editMode ? "Fertig" : "Bearbeiten";
  }

  openCreateModal(): void {
    this.createModalRef = this.modalService.show(this.createModal);
  }

  openRepeatingModal(): void {
    this.repeatingModalRef = this.modalService.show(this.createRepeatModal);
  }

  openTextModal(): void {
    this.textModalRef = this.modalService.show(this.createTextModal);
    this.modalService.hide(this.createModalRef?.id);
  }

  closeCreateModal(): void {
    this.modalService.hide(this.createModalRef?.id);
  }

  closeRepeatingModal(): void {
    this.modalService.hide(this.repeatingModalRef?.id);
  }

  closeTextModal(): void {
    this.createModalRef = this.modalService.show(this.createModal);
    this.modalService.hide(this.textModalRef?.id);
  }

  closeAllModals(): void {
    this.modalService.hide(this.repeatingModalRef?.id);
    this.modalService.hide(this.createModalRef?.id);
  }

  rtrim(input: string, characters: string): string {
    let end = input.length - 1;
    while (characters.indexOf(input[end]) >= 0) {
      end -= 1;
    }
    return input.substr(0, end + 1);
  }

}
