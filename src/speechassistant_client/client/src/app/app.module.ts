import { HttpClientModule } from '@angular/common/http';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { BrowserModule, Title } from '@angular/platform-browser';
import { RouterModule, Routes } from "@angular/router";
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
import { MatCheckboxModule } from "@angular/material/checkbox";
import { AccordionModule } from 'ngx-bootstrap/accordion';
import { AlertModule,AlertConfig } from 'ngx-bootstrap/alert';
import { ButtonsModule } from 'ngx-bootstrap/buttons';
import { CarouselModule } from 'ngx-bootstrap/carousel';
import { CollapseModule } from 'ngx-bootstrap/collapse';
import { BsDatepickerModule, BsDatepickerConfig } from 'ngx-bootstrap/datepicker';
import { BsDropdownModule,BsDropdownConfig } from 'ngx-bootstrap/dropdown';
import { ModalModule, BsModalService } from 'ngx-bootstrap/modal';
import { TooltipModule } from 'ngx-bootstrap/tooltip';
// import { AppBootstrapModule } from './app-bootstrap/app-bootstrap.module';
import { FormsModule } from "@angular/forms";
import { AlarmsComponent } from "../lib/pages/alarms/alarms.component";
import { AlarmComponent } from "../lib/pages/alarm/alarm.component";
import {TimepickerModule} from "ngx-bootstrap/timepicker";
import {NgxMaterialTimepickerModule} from 'ngx-material-timepicker';

const routes: Routes = [
  { path: 'alarms', component: AlarmsComponent },
  { path: 'alarms/:id', component: AlarmComponent },
  { path: 'routines', component: RoutinesComponent }
]

@NgModule({
  declarations: [
    AppComponent, RoutinesComponent, RoutineComponent, TileSelectorComponent, AlarmsComponent, AlarmComponent
  ],
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        LayoutModule,
        MatToolbarModule,
        MatButtonModule,
        MatSidenavModule,
        MatIconModule,
        MatListModule,
        MatTimepickerModule,
        MatCheckboxModule,
        HttpClientModule,
        BrowserModule,
        BsDropdownModule.forRoot(),
        TooltipModule.forRoot(),
        ModalModule.forRoot(),
        //AppBootstrapModule,
        AccordionModule,
        AlertModule,
        ButtonsModule,
        FormsModule,
        CarouselModule,
        CollapseModule,
        BsDatepickerModule.forRoot(),
        BsDropdownModule,
        ModalModule,
        RouterModule.forRoot(routes),
        TimepickerModule,
        NgxMaterialTimepickerModule
    ],
  providers: [Title],
  bootstrap: [AppComponent],
  exports: [

  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class AppModule { }
