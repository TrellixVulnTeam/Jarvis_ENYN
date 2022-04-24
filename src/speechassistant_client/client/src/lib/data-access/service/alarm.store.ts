
import {Injectable} from '@angular/core';
import {BehaviorSubject, filter, Observable, Observer, Subject} from 'rxjs';
import {Alarm} from "../models/alarm";
import {BackendService} from "./backend.service";
import {map} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class AlarmStore {

  alarms: Alarm[] = [];
  alarmChange$: Subject<Alarm[]> = new Subject<Alarm[]>();

  constructor( private backendService: BackendService ) { }

  getAlarm( id: number ): Observable<Alarm> {
    return this.alarmChange$.pipe(
      map( alarms => {
        let index: number = this.alarms.findIndex( alarm => alarm.id === id );
        return alarms[ index ];
      } )
    );
  }

  getAlarms( ): Subject<Alarm[]> {
    this.alarmChange$.next(this.alarms);
    return this.alarmChange$;
  }

  loadAndGetAlarms( ): Subject<Alarm[]> {
    this.backendService.loadAlarms().subscribe(alarms => this.alarms = alarms);
    this.alarmChange$.next(this.alarms);
    return this.alarmChange$;
  }

  addAlarm( newAlarm: Alarm ): void {
    this.alarms.push( newAlarm );
    this.alarmChange$.next(this.alarms);
    this.backendService.createAlarm( newAlarm ).subscribe(resultSet => {
      newAlarm.id = resultSet.id;
      newAlarm.text = resultSet.text; // in case that the input was malicious
    });
    this.alarmChange$.next(this.alarms);
  }

  updateAlarm( newAlarm: Alarm ): void {

    this.alarmChange$.next(this.alarms);
  }

  updateAlarmActiveStatus( id: number, newStatus: boolean ): void {
    this.alarmChange$.next(this.alarms);
  }

  deleteAlarm( id: number ): void {
    let index: number = this.alarms.findIndex(item => item.id === id);
    this.alarms.splice(index, 1);
    this.alarmChange$.next(this.alarms);
    this.backendService.deleteAlarm(id).subscribe();
  }

}
