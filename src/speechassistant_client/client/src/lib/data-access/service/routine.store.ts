
import {Injectable} from '@angular/core';
import {BehaviorSubject, Observable, Subject} from 'rxjs';
import {Alarm} from "../models/alarm";
import {Routine} from "../models";
import {BackendService} from "./backend.service";

@Injectable({
  providedIn: 'root'
})
export class RoutineStore {

  routines: Routine[] = [];
  routineSubject: Subject<Routine[]> = new Subject<Routine[]>();

  constructor( private backendService: BackendService ) {
    this.backendService.loadAllRoutines().subscribe( routines => {
      this.routineSubject.next( routines );
      this.routines = routines;
    });
  }

  getRoutine( name: string ): Observable<Routine> {
    let index: number = this.routines.findIndex( routine => routine.name === name );
    return new Observable( observer => observer.next(this.routines[ index ]));
  }

  getRoutines( ): Subject<Routine[]> {
    this.routineSubject.next( this.routines );
    return this.routineSubject;
  }

  loadAndGetRoutines( ): Subject<Routine[]> {
    this.backendService.loadAllRoutines().subscribe(routines => {
      this.routineSubject.next( routines );
      this.routines = routines;
    });

    return this.routineSubject;
  }

  addRoutine( newRoutine: Routine ): Subject<Routine[]> {
    this.routines.push( newRoutine );
    this.routineSubject.next( this.routines );
    this.backendService.createRoutine( newRoutine ).subscribe(resultSet => {
      newRoutine.name = resultSet.name;
    });
    this.routineSubject.next( this.routines );
    return this.routineSubject;
  }

  updateRoutine( newRoutine: Routine ): void {
    let index: number = this.routines.findIndex( routine => routine.name === newRoutine.name );
    this.routines[ index ] = newRoutine;
    this.routineSubject.next( this.routines );
    this.backendService.updateRoutine( newRoutine ).subscribe( );
  }

  deleteRoutine( name: string ): void {
    let index: number = this.routines.findIndex(item => item.name === name);
    this.routines.splice(index, 1);
    this.routineSubject.next( this.routines );
    this.backendService.deleteRoutine( name ).subscribe( );
  }

}
