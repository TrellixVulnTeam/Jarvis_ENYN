
import {Injectable} from '@angular/core';
import {async, BehaviorSubject, filter, Observable, Observer, Subject} from 'rxjs';
import {Alarm} from "../models/alarm";
import {BackendService} from "./backend.service";
import {map} from "rxjs/operators";
import {NONE_TYPE} from "@angular/compiler";
import {chunkByNumber} from "ngx-bootstrap/carousel/utils";

@Injectable({
  providedIn: 'root'
})
export class AlarmStore {

  alarms: Alarm[] = [];
  alarmSubject: Subject<Alarm[]> = new Subject<Alarm[]>();

  constructor( private backendService: BackendService ) {
    this.backendService.loadAlarms().subscribe( alarms => {
      this.alarmSubject.next( alarms );
      this.alarms = alarms;
    });
  }

  getAlarm( id: number ): Observable<Alarm> {
      const alarm: Subject<Alarm> = new Subject<Alarm>();
      if (this.alarms.length == 0) {
        this.backendService.loadAlarms().subscribe(alarms => {
          this.alarmSubject.next( alarms );
          this.alarms = alarms;
          let index: number = this.alarms.findIndex( alarm => alarm.id == id );
          alarm.next(alarms[ index ]);
        });
      }
      let index: number = this.alarms.findIndex( alarm => alarm.id == id );
      alarm.next( this.alarms[ index ] );
      return alarm;
  }

  getAlarms( ): Subject<Alarm[]> {
      this.alarmSubject.next( this.alarms );
      return this.alarmSubject;
  }

  loadAndGetAlarms( ): Observable<Alarm[]> {
    this.backendService.loadAlarms().subscribe(alarms => {
      this.alarmSubject.next( alarms );
      this.alarms = alarms;
    });

    return this.alarmSubject;
  }

  addAlarm( newAlarm: Alarm ): void {
    this.alarms.push( newAlarm );
    this.alarmSubject.next( this.alarms );
    this.backendService.createAlarm( newAlarm ).subscribe(resultSet => {
      newAlarm.id = resultSet.id;
      newAlarm.text = resultSet.text; // in case that the input was malicious
    });
    this.alarmSubject.next( this.alarms );
  }

  updateAlarm( newAlarm: Alarm ): void {
    let index: number = this.alarms.findIndex( alarm => alarm.id === newAlarm.id );
    this.alarms[ index ] = newAlarm;
    this.alarmSubject.next( this.alarms );
    this.backendService.updateAlarm( newAlarm ).subscribe( );
  }

  updateAlarmActiveStatus( id: number, newStatus: boolean ): void {
    let index: number = this.alarms.findIndex( alarm => alarm.id === id );
    this.alarms[ index ].active = newStatus;
    this.alarmSubject.next( this.alarms );
    this.backendService.updateAlarmActiveState( id, newStatus ).subscribe( );
  }

  deleteAlarm( id: number ): void {
    let index: number = this.alarms.findIndex(item => item.id === id);
    this.alarms.splice(index, 1);
    this.alarmSubject.next( this.alarms );
    this.backendService.deleteAlarm( id ).subscribe( );
  }

}
