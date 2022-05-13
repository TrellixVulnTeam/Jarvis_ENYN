import {BrowserModule} from "@angular/platform-browser";
import {NgModule} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {RouterModule} from "@angular/router";
import {MatIconModule} from "@angular/material/icon";
import {AlarmComponent} from "./alarm.component";
import {MatTimepickerModule} from "mat-timepicker";

@NgModule({
  declarations: [
    AlarmComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    RouterModule,
    MatIconModule,
    MatTimepickerModule,
  ],
  providers: [],
  bootstrap: [],
  exports: [AlarmComponent]
})
export class AlarmModule {
}
