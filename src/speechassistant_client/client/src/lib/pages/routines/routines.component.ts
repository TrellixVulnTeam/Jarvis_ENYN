
import {Component, Input} from "@angular/core";
import { Routine } from "../../data-access/models";

@Component({
  selector: 'routines',
  templateUrl: './routines.component.html',
  styleUrls: ['./routines.component.scss']
})
export class RoutinesComponent {

  title: string = "Routinen";

  @Input() routines: Routine[] = [];

}
