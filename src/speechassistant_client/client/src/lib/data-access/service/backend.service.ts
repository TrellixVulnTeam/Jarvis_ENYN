
import {HttpClient, HttpEvent, HttpRequest, HttpResponse} from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable, retry} from 'rxjs';
import { Routine } from '../models';
import {Router} from "@angular/router";
import {JsonObject} from "@angular/compiler-cli/ngcc/src/packages/entry_point";
import {Alarm} from "../models/alarm";
import {temporaryAllocator} from "@angular/compiler/src/render3/view/util";
import {map} from "rxjs/operators";

@Injectable({
  providedIn: 'root',
})
export class BackendService {
  readonly url: string = 'http://localhost:4200/api/v1/'

  constructor(private httpClient: HttpClient) { }

  loadRoutine(name: string): Observable<Routine> {
    return this.httpClient.get<Routine>(this.url + 'routines/'+name);
  }

  loadAllRoutines(): Observable<Routine[]> {
    return this.httpClient.get<Routine[]>(this.url + 'routines/').pipe(
      map ((routines: Routine[]) => {
        for (let i = 0; i < routines.length; i++) {
          // @ts-ignore
            let dates: JsonObject[] = routines[i].dateOfDay;
            // @ts-ignore
            let times: JsonObject[] = routines[i].clock_time;
            routines[i].dateOfDay = [];
            routines[i].clock_time = [];

            dates.forEach(date => {
              let newDate: Date = new Date();
              newDate.setMonth(date["month"] as number);
              newDate.setDate(date["day"] as number);
              routines[i].dateOfDay.push(newDate);
            });

            times.forEach(time => {
              let newTime: Date = new Date();
              newTime.setHours(time["hour"] as number);
              newTime.setMinutes(time["minute"] as number);
              routines[i].dateOfDay.push(newTime);
            });
        }
        return routines;
    })
    );
  }

  createRoutine(routine: Routine): Observable<Routine> {
    let routinePayload = BackendService.getRoutinePayload(routine);

    return this.httpClient.post<Routine>(this.url + 'routines/', routinePayload);
  }

  deleteRoutine(name: string): Observable<void> {
    return this.httpClient.delete<void>(this.url + 'routines/' + name);
  }

  updateRoutine(routine: Routine): Observable<Routine> {
    let routinePayload = BackendService.getRoutinePayload(routine);
    return this.httpClient.put<Routine>(this.url + 'routines/', routinePayload);
  }

  loadAlarms(): Observable<Alarm[]> {
    return this.httpClient.get<Alarm[]>(this.url + 'alarms/').pipe(
      map (alarms => {
        alarms.forEach(alarm => {
          // @ts-ignore
          let hours = alarm.time["hour"] as number;
          // @ts-ignore
          let minutes = alarm.time["minute"] as number;
          alarm.time = new Date();
          alarm.time.setHours(hours);
          alarm.time.setMinutes(minutes);
        })
        return alarms;
      }));
  }

  loadAlarmWithId(id: number): Observable<Alarm> {
    return this.httpClient.get<Alarm>(this.url + 'alarms/'+id)
  }

  createAlarm(alarm: Alarm): Observable<Alarm> {
    let alarmPayload = BackendService.getAlarmPayload(alarm);
    return this.httpClient.post<Alarm>(this.url + 'alarms/', alarmPayload);
  }

  deleteAlarm(id: number): Observable<Alarm> {
    return this.httpClient.delete<Alarm>(this.url + 'alarms/'+id);
  }

  updateAlarm(alarm: Alarm): Observable<Alarm> {
    let alarmPayload = BackendService.getAlarmPayload(alarm);
    return this.httpClient.put<Alarm>(this.url + 'alarms/', alarmPayload);
  }

  updateAlarmActiveState(id: number, active: boolean): Observable<any> {
    let alarmPayload = { "active": active };
    return this.httpClient.put<any>(this.url + 'alarms/'+id, alarmPayload);
  }

  private static getRoutinePayload(routine: Routine): JsonObject {
    let dateOfDays: JsonObject[] = [];
    routine.dateOfDay.forEach(item => {
      let jsonDate: JsonObject = {
        "day": item.getDay(),
        "month": item.getMonth()
      }
      dateOfDays.push(jsonDate);
    });

    let clockTimes: JsonObject[] = [];
    routine.clock_time.forEach(item => {
      let jsonDate: JsonObject = {
        "hour": item.getHours(),
        "minute": item.getMinutes()
      }
      dateOfDays.push(jsonDate);
    });

    return {
      "name": routine.name,
      "description": routine.description,
      "retakes": {
        "days": {
          "monday": routine.monday,
          "tuesday": routine.tuesday,
          "wednesday": routine.wednesday,
          "thursday": routine.thursday,
          "friday": routine.friday,
          "saturday": routine.saturday,
          "sunday": routine.sunday,
          "date_of_day": dateOfDays
        }
      },
      "activation": {
        "clock_time": clockTimes,
        "after_alarm": routine.after_alarm,
        "after_sunrise": routine.after_sunrise,
        "after_sunset": routine.after_sunset,
        "after_call": routine.after_call
      },
      "actions": {
        "commands": routine.commands
      }
    };
  }

  private static getAlarmPayload(alarm: Alarm): JsonObject {
    return {
      "time": {
        "hour": alarm.time.getHours(),
        "minute": alarm.time.getMinutes(),
        "total_seconds": alarm.time.getHours()*3600+alarm.time.getMinutes()*60
      },
      "repeating": {
        "monday": alarm.monday,
        "tuesday": alarm.tuesday,
        "wednesday": alarm.wednesday,
        "thursday": alarm.thursday,
        "friday": alarm.friday,
        "saturday": alarm.saturday,
        "sunday": alarm.sunday,
        "regular": alarm.regular
      },
      "text": alarm.text,
      "sound": alarm.sound
    }
  }

  getAllModuleNames(): Observable<string[]> {
    return this.httpClient.get<string[]>(this.url + 'modules/names');
  }

}


