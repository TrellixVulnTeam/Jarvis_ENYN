import {Component, Input} from "@angular/core";
import {Light} from "../../../data-access/models/light";

@Component({
  selector: 'light',
  templateUrl: './light.component.html',
  styleUrls: ['./light.component.scss']
})
export class LightComponent{

  // @ts-ignore
  @Input() light: Light;


  constructor() {

  }


}
