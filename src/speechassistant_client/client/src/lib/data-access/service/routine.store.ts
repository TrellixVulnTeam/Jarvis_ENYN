
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
  routineChange$: Subject<Routine[]> = new Subject<Routine[]>();

  constructor( private backendService: BackendService ) { }

  getRoutine( name: string ): Observable<Routine> {
    let index: number = this.routines.findIndex( routine => routine.name === name );
    return new Observable( observer => observer.next(this.routines[ index ]));
  }

  getRoutines( ): Subject<Routine[]> {
    this.routineChange$.next(this.routines);
    return this.routineChange$;
  }

  loadAndGetRoutines( ): Subject<Routine[]> {
    this.backendService.loadAllRoutines().subscribe((routines: Routine[]) => this.routines = routines);
    this.routineChange$.next( this.routines );
    return this.routineChange$;
  }

  addRoutine( newRoutine: Routine ): void {
    this.routineChange$.next(this.routines);
  }

  updateRoutine( newRoutine: Routine ): void {
    this.routineChange$.next(this.routines);
  }

  deleteRoutine( name: string ): void {
    this.routineChange$.next(this.routines);
  }

}
