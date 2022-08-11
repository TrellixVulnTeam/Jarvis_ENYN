import {Injectable} from '@angular/core';
import {ReplaySubject} from 'rxjs';
import {BackendService} from "../backend.service";

@Injectable({
  providedIn: 'root'
})
export class ModuleStore {

  moduleNames: string[] = [];
  moduleNamesSubject: ReplaySubject<string[]> = new ReplaySubject<string[]>();

  constructor(private backendService: BackendService) {
  }

  loadModuleNames(): ReplaySubject<string[]> {
    if (this.moduleNames.length == 0) {
      this.backendService.loadModuleNames().subscribe(moduleNames => {
        this.moduleNames = moduleNames;
        this.moduleNamesSubject.next(moduleNames);
      });
    } else {
      this.moduleNamesSubject.next(this.moduleNames);
    }

    return this.moduleNamesSubject;
  }

}
