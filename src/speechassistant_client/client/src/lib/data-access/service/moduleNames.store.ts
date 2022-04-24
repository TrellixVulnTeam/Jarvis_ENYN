
import {Injectable} from '@angular/core';
import {BehaviorSubject, Observable} from 'rxjs';
import {Alarm} from "../models/alarm";
import {Routine} from "../models";
import {BackendService} from "./backend.service";

@Injectable({
  providedIn: 'root'
})
export class ModuleNamesStore {

  moduleNames: string[] = [];

  constructor( private backendService: BackendService ) { }

  getModuleNames( ): Observable<string[]> {
    return new Observable( observer => observer.next(this.moduleNames));
  }

  loadAndGetModuleNames( ): Observable<string[]> {
    this.backendService.getAllModuleNames().subscribe(modules => {
      this.moduleNames = modules;
    });
    return new Observable( observer => observer.next(this.moduleNames));
  }

}
