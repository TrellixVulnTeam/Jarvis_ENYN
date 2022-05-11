import {Component, Input, OnInit} from "@angular/core";
import {LightStore} from "../../data-access/service/light.store";
import {Light} from "../../data-access/models/light";
import {LightGroup} from "../../data-access/models/lightGroup";

@Component({
  selector: 'phue',
  templateUrl: './phue.component.html',
  styleUrls: ['./phue.component.scss']
})
export class PhueComponent implements OnInit {
  // @ts-ignore
  groups: LightGroup[];
  // @ts-ignore
  lights: Light[];

  constructor(private lightsStore: LightStore) {

  }

  ngOnInit() {
    this.lightsStore.getAllLights().subscribe(lights => this.lights = lights);
    this.lightsStore.getAllGroups().subscribe(groups => this.groups = groups);
  }

}
