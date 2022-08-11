import {HttpClientModule} from '@angular/common/http';
import {NgModule} from '@angular/core';
import {BrowserModule, Title} from '@angular/platform-browser';
import {RouterModule, Routes} from "@angular/router";
import {AppComponent} from './app.component';

import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {LayoutModule} from '@angular/cdk/layout';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatIconModule} from '@angular/material/icon';
import {MatListModule} from '@angular/material/list';
import {RoutinesComponent} from "../lib/pages/routines/routines.component";
import {MatCheckboxModule} from "@angular/material/checkbox";
import {AccordionModule} from 'ngx-bootstrap/accordion';
import {AlertModule} from 'ngx-bootstrap/alert';
import {ButtonsModule} from 'ngx-bootstrap/buttons';
import {CarouselModule} from 'ngx-bootstrap/carousel';
import {CollapseModule} from 'ngx-bootstrap/collapse';
import {BsDatepickerModule} from 'ngx-bootstrap/datepicker';
import {BsDropdownModule} from 'ngx-bootstrap/dropdown';
import {ModalModule} from 'ngx-bootstrap/modal';
import {TooltipModule} from 'ngx-bootstrap/tooltip';
import {FormsModule} from "@angular/forms";
import {AlarmsComponent} from "../lib/pages/alarms/alarms.component";
import {AlarmComponent} from "../lib/pages/alarm/alarm.component";
import {TimepickerModule} from "ngx-bootstrap/timepicker";
import {AlarmsModule} from "../lib/pages/alarms/alarms.module";
import {PhueModule} from "../lib/pages/phue/phue.module";
import {RoutinesModule} from "../lib/pages/routines/routines.module";
import {AlarmModule} from "../lib/pages/alarm/alarm.module";

const routes: Routes = [
  {path: 'alarms', component: AlarmsComponent},
  {path: 'alarms/:id', component: AlarmComponent},
  {path: 'routines', component: RoutinesComponent}
]

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    LayoutModule,
    MatToolbarModule,
    MatSidenavModule,
    MatListModule,
    MatCheckboxModule,
    HttpClientModule,
    BrowserModule,
    BsDropdownModule.forRoot(),
    TooltipModule.forRoot(),
    ModalModule.forRoot(),
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
    AlarmsModule,
    PhueModule,
    RoutinesModule,
    MatIconModule,
    AlarmModule
  ],
  providers: [Title],
  bootstrap: [AppComponent]
})
export class AppModule {
}
