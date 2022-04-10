import { NgModule } from '@angular/core';
import { BrowserModule, Title } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';


import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LayoutModule } from '@angular/cdk/layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { RoutinesComponent } from "../lib/pages/routines/routines.component";
import { RoutineComponent } from "../ui/routine/routine.component";
import { MatTimepickerModule } from "mat-timepicker";
import { TileSelectorComponent } from "../ui/tile-selector/tileSelector.component";
import {MatCheckboxModule} from "@angular/material/checkbox";


@NgModule({
  declarations: [
    AppComponent, RoutinesComponent, RoutineComponent, TileSelectorComponent
  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        BrowserAnimationsModule,
        LayoutModule,
        MatToolbarModule,
        MatButtonModule,
        MatSidenavModule,
        MatIconModule,
        MatListModule,
        MatTimepickerModule,
        MatCheckboxModule
    ],
  providers: [Title],
  exports: [

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
