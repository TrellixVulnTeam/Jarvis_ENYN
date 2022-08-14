
import {Injectable} from '@angular/core';
import {async, BehaviorSubject, filter, Observable, Observer, Subject} from 'rxjs';
import {Alarm} from "../../models/alarm";
import {BackendService} from "../backend.service";
import {map} from "rxjs/operators";
import {NONE_TYPE} from "@angular/compiler";
import {chunkByNumber} from "ngx-bootstrap/carousel/utils";
import {Light} from "../../models/light";
import {LightGroup} from "../../models/lightGroup";

@Injectable({
  providedIn: 'root'
})
export class LightStore {

  lights: Light[] = [];
  lightsSubject: Subject<Light[]> = new Subject<Light[]>();
  groups: LightGroup[] = [];
  groupsSubject: Subject<LightGroup[]> = new Subject<LightGroup[]>();

  constructor( private backendService: BackendService ) {
    this.backendService.loadAllLights().subscribe( lights => {
      this.lightsSubject.next( lights );
      this.lights = lights;
    });
  }

  getLightById(id: number): Subject<Light> {
    const lightSubject = new Subject<Light>();
    let index = this.lights.findIndex(light => light.id === id);
    if (index === -1) {
      this.backendService.loadLightById(id).subscribe(light => {
        lightSubject.next(light);
      });
    } else {
      lightSubject.next(this.lights[index]);
    }

    return lightSubject;
  }

  getAllLights(): Subject<Light[]> {
    if (this.lights == []) {
      this.backendService.loadAllLights().subscribe(lights => {
        this.lights = lights;
        this.lightsSubject.next(this.lights);
      });
    }
    return this.lightsSubject;
  }

  getGroupById(id: number): Subject<LightGroup> {
    const groupSubject = new Subject<LightGroup>();
    let index = this.groups.findIndex(group => group.id === id);
    if (index === -1) {
      this.backendService.loadGroupById(id).subscribe(group => {
        groupSubject.next(group);
      })
    }
    return groupSubject;
  }

  getAllGroups(): Subject<LightGroup[]> {
    if (this.groups == []) {
      this.backendService.loadAllGroups().subscribe(groups => {
        this.groups = groups;
        this.groupsSubject.next(this.groups);
      })
    }
    return this.groupsSubject;
  }

  updateLightById(id: number, color: string, powerState: boolean, brightness: number, temperature: number): void {
    this.backendService.updateLightById(id, color, powerState, brightness, temperature).subscribe();
    let index = this.lights.findIndex(light => light.id === id);
    if (index === -1) {
      this.backendService.loadLightById(id).subscribe(light => {
        this.lights.push(light);
      });
    } else {
      this.lights[index].color = color;
      this.lights[index].powerState = powerState;
      this.lights[index].brightness = brightness;
      this.lights[index].temperature = temperature;
    }
  }

  updateAllLights(color: string, powerState: boolean, brightness: number, temperature: number): void {
    this.backendService.updateAllLights(color, powerState, brightness, temperature);
    this.lights.forEach(light => {
      light.color = color;
      light.brightness = brightness;
      light.temperature = temperature;
      light.powerState = powerState;
    });
  }

  updateGroup(id: number, color: string, powerState: boolean, brightness: number, temperature: number): void {

  }



}
