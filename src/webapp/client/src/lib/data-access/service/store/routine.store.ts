import {Injectable} from '@angular/core';
import {ReplaySubject, Subject} from 'rxjs';
import {Routine} from "../../models";
import {BackendService} from "../backend.service";

@Injectable({
  providedIn: 'root'
})
export class RoutineStore {

  routines: Routine[] = [];
  routineSubject: ReplaySubject<Routine[]> = new ReplaySubject<Routine[]>(1);

  constructor(private backendService: BackendService) {
    this.backendService.loadAllRoutines().subscribe(routines => {
      this.routineSubject.next(routines);
      this.routines = routines;
    });
  }

  loadRoutines(): Subject<Routine[]> {
    if (this.routines.length == 0) {
      this.backendService.loadAllRoutines().subscribe(routines => {
        this.routines = routines;
        this.routineSubject.next(this.routines);
      })
    } else {
      this.routineSubject.next(this.routines);
    }
    return this.routineSubject;
  }

  addRoutine(newRoutine: Routine): ReplaySubject<Routine[]> {
    this.routines.push(newRoutine);
    this.routineSubject.next(this.routines);
    this.backendService.createRoutine(newRoutine).subscribe(resultSet => {
      newRoutine.name = resultSet.name;
    });
    this.routineSubject.next(this.routines);
    return this.routineSubject;
  }

  updateRoutine(newRoutine: Routine): ReplaySubject<Routine[]> {
    let index: number = this.routines.findIndex(routine => routine.name === newRoutine.name);
    this.routines[index] = newRoutine;
    this.routineSubject.next(this.routines);
    this.backendService.updateRoutine(newRoutine).subscribe();
    return this.routineSubject;
  }

  deleteRoutine(name: string): ReplaySubject<Routine[]> {
    let index: number = this.routines.findIndex(item => item.name === name);
    this.routines.splice(index, 1);
    this.routineSubject.next(this.routines);
    this.backendService.deleteRoutine(name).subscribe();
    return this.routineSubject;
  }

}
