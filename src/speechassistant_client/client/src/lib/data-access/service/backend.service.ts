
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Routine } from '../models';
import {Router} from "@angular/router";
import {JsonObject} from "@angular/compiler-cli/ngcc/src/packages/entry_point";

@Injectable({
  providedIn: 'root',
})
export class BackendService {
  readonly url: string = 'http://localhost:4200/api/v1/'

  constructor(private httpClient: HttpClient) { }

  loadRoutine(name: string): Observable<Routine> {
    return this.httpClient.get<Routine>(this.url + 'routine/'+name);
  }

  loadAllRoutines(): Observable<Routine[]> {
    return this.httpClient.get<Routine[]>(this.url + 'routine/');
  }

  createRoutine(routine: Routine): Observable<Routine> {
    let routinePayload = BackendService.getRoutinePayload(routine);

    return this.httpClient.post<Routine>(this.url + 'routine/', routinePayload);
  }

  deleteRoutine(name: string): Observable<void> {
    return this.httpClient.delete<void>(this.url + 'routine/' + name);
  }

  updateRoutine(routine: Routine): Observable<Routine> {
    let routinePayload = BackendService.getRoutinePayload(routine);
    return this.httpClient.put<Routine>(this.url + 'routine/', routinePayload);
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
  getAllModuleNames(): Observable<string[]> {
    return this.httpClient.get<string[]>(this.url + 'modules/names');
  }
}


