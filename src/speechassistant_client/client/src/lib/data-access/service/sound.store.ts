
import {Injectable} from '@angular/core';
import {BackendService} from "./backend.service";
import {Subject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class SoundStore {

  soundNames: string[] = [];
  soundNamesSubject: Subject<string[]> = new Subject<string[]>();

  constructor( private backendService: BackendService ) {
    this.backendService.loadAllSounds().subscribe( soundNames => {
      this.soundNames = soundNames;
      this.soundNamesSubject.next( soundNames );
    } );
  }

  loadSoundNames( ): Subject<string[]> {
    this.soundNamesSubject.next( this.soundNames );
    return this.soundNamesSubject;
  }

}
