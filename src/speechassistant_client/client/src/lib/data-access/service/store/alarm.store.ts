import {Injectable} from '@angular/core';
import {ReplaySubject, Subject} from 'rxjs';
import {Alarm} from "../../models/alarm";
import {BackendService} from "../backend.service";

@Injectable({
  providedIn: 'root'
})
export class AlarmStore {

  alarms: Alarm[] = [];
  alarmSubject: ReplaySubject<Alarm[]> = new ReplaySubject<Alarm[]>(1);

  constructor(private backendService: BackendService) {
  }

  getAlarm(id: number): ReplaySubject<Alarm> {
    const singleAlarmSubject: ReplaySubject<Alarm> = new ReplaySubject<Alarm>(1);
    let index: number = this.alarms.findIndex(alarm => alarm.id == id);
    if (index == -1) {
      this.backendService.loadAlarmWithId(id).subscribe(alarm => {
        singleAlarmSubject.next(alarm);
      });
    } else {
      singleAlarmSubject.next(this.alarms[index]);
    }
    return singleAlarmSubject;
  }

  getAlarms(): ReplaySubject<Alarm[]> {
    if (this.alarms.length == 0) {
      this.backendService.loadAlarms().subscribe(alarms => {
        this.alarms = alarms;
        this.alarmSubject.next(this.alarms);
      })
    } else {
      this.alarmSubject.next(this.alarms);
    }
    return this.alarmSubject;
  }

  addAlarm(newAlarm: Alarm): void {
    this.alarms.push(newAlarm);
    this.alarmSubject.next(this.alarms);
    this.backendService.createAlarm(newAlarm).subscribe(resultSet => {
      let index = this.alarms.findIndex(alarm => alarm == newAlarm);
      // @ts-ignore
      let location = resultSet.headers.get('location');
      let id = location?.substr(location?.lastIndexOf('/') + 1);
      // @ts-ignore
      this.alarms[index].id = id as number;
      this.alarmSubject.next(this.alarms);
    });
  }

  updateAlarm(newAlarm: Alarm): void {
    let index: number = this.alarms.findIndex(alarm => alarm.id === newAlarm.id);
    this.alarms[index] = newAlarm;
    this.alarmSubject.next(this.alarms);
    this.backendService.updateAlarm(newAlarm).subscribe();
  }

  updateAlarmActiveStatus(id: number, newStatus: boolean): void {
    let index: number = this.alarms.findIndex(alarm => alarm.id === id);
    this.alarms[index].active = newStatus;
    this.alarmSubject.next(this.alarms);
    this.backendService.updateAlarmActiveState(id, newStatus).subscribe();
  }

  deleteAlarm(id: number): Subject<Alarm[]> {
    let index: number = this.alarms.findIndex(item => item.id === id);
    if (index != -1) {
      this.alarms.splice(index, 1);
      this.alarmSubject.next(this.alarms);
      this.backendService.deleteAlarm(id).subscribe();
    }
    return this.alarmSubject;
  }

}
