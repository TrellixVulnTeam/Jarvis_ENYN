import {BrowserModule} from "@angular/platform-browser";
import { NgModule } from '@angular/core';
import {AlarmsComponent} from "./alarms.component";
import {TimepickerModule} from "ngx-bootstrap/timepicker";
import {FormsModule} from "@angular/forms";
import {RouterModule} from "@angular/router";
import {AlarmComponent} from "./alarm/alarm.component";
import {MatIconModule} from "@angular/material/icon";

@NgModule({
  declarations: [
    AlarmsComponent, AlarmComponent
  ],
  imports: [
    BrowserModule,
    TimepickerModule.forRoot(),
    FormsModule,
    RouterModule,
    MatIconModule,
  ],
  providers: [],
  bootstrap: [],
  exports: [AlarmsComponent]
})
export class AlarmsModule { }
