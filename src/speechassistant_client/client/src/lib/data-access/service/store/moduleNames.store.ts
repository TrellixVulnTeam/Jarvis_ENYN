
import {Injectable} from '@angular/core';
import {BehaviorSubject, Observable, Subject} from 'rxjs';
import {Alarm} from "../../models/alarm";
import {Routine} from "../../models";
import {BackendService} from "../backend.service";

@Injectable({
  providedIn: 'root'
})
export class ModuleNamesStore {

  moduleNames: string[] = [];
  moduleNamesSubject: Subject<string[]> = new Subject<string[]>();

  constructor( private backendService: BackendService ) {
    this.backendService.loadAllModuleNames().subscribe( moduleNames =>this.moduleNames = moduleNames );
  }

  loadModuleNames( ): Subject<string[]> {
    this.moduleNamesSubject.next( this.moduleNames );
    return this.moduleNamesSubject;
  }

}
