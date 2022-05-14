import {NgModule} from "@angular/core";
import {RoutinesComponent} from "./routines.component";
import {RoutineComponent} from "./routine/routine.component";
import {FormsModule} from "@angular/forms";
import {RouterModule} from "@angular/router";
import {BrowserModule} from "@angular/platform-browser";
import {TileSelectorComponent} from "../../../ui/tile-selector/tileSelector.component";
import {MatTimepickerModule} from "mat-timepicker";
import {MatIconModule} from "@angular/material/icon";
import {TimepickerModule} from "ngx-bootstrap/timepicker";


@NgModule({
  declarations: [
    RoutinesComponent, RoutineComponent, TileSelectorComponent
  ],
  imports: [
    BrowserModule,
    MatTimepickerModule,
    FormsModule,
    RouterModule,
    MatIconModule,
    TimepickerModule
  ],
  providers: [],
  bootstrap: [],
  exports: [RoutinesComponent]
})
export class RoutinesModule {
}
