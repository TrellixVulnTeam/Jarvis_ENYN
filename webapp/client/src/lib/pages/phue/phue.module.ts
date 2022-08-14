import {BrowserModule} from "@angular/platform-browser";
import {NgModule} from "@angular/core";
import {LightComponent} from "./light/light.component";
import {PhueComponent} from "./phue.component";
import {GroupComponent} from "./group/group.component";

@NgModule({
  declarations: [
    PhueComponent, LightComponent, GroupComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [],
  exports: [PhueComponent]
})
export class PhueModule { }
