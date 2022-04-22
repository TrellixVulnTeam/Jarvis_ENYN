
import {Component, Input, OnInit, TemplateRef} from "@angular/core";
import { Routine } from "../../data-access/models";
import {BackendService} from "../../data-access/service/backend.service";
import { BsModalService, BsModalRef } from 'ngx-bootstrap/modal';
import {Command} from "../../data-access/models/command";
import {materialModuleSpecifier} from "@angular/material/schematics/ng-update/typescript/module-specifiers";
import {retry} from "rxjs";
import {JsonObject} from "@angular/compiler-cli/ngcc/src/packages/entry_point";
import {Title} from "@angular/platform-browser";

@Component({
  selector: 'routines',
  templateUrl: './routines.component.html',
  styleUrls: ['./routines.component.scss']
})
export class RoutinesComponent implements OnInit{

  title: string = "Routinen";
  emptyRoutine: Routine = {name:"", description:"", onCommands:[], monday:false, tuesday:false, wednesday:false, thursday:false, friday:false, saturday:false, sunday:false, dateOfDay:[], clock_time:[], after_alarm:false, after_sunrise:false, after_sunset:false, after_call:false, commands:[]}
  emptyCommands: Command[] = [];
  modalRef?: BsModalRef;
  postRoutine: boolean = false;
  moduleNames: string[] = [];

  @Input() routines: Routine[];

  constructor(private titleService: Title, private backendService: BackendService, private modalService: BsModalService) { }

  ngOnInit(): void {
    this.titleService.setTitle('Routinen Übersicht');
    this.backendService.loadAllRoutines().subscribe((routines: Routine[]) =>
    {
      this.routines = routines;
      for (let i = 0; i < this.routines.length; i++) {
        // @ts-ignore
        let dates: JsonObject[] = this.routines.dateOfDay;
        // @ts-ignore
        let times: JsonObject[] = this.routines.clock_time;
        this.routines[i].dateOfDay = [];
        this.routines[i].clock_time = [];

        dates.forEach(date => {
          let newDate: Date = new Date();
          newDate.setMonth(date["month"] as number);
          newDate.setDate(date["day"] as number);
          routines[i].dateOfDay.push(newDate);
        });

        times.forEach(time => {
          let newTime: Date = new Date();
          newTime.setHours(time["hour"] as number);
          newTime.setMinutes(time["minute"] as number);
          routines[i].dateOfDay.push(newTime);
        });
      }
    });
    /*this.backendService.getAllModuleNames().subscribe(modules => {
      this.moduleNames = modules;
    });*/
  }

  openModal(template: TemplateRef<any>, modalSize: string = ""): void {
    if (modalSize != "") {
      this.modalRef = this.modalService.show(template, {"animated": true, "class": "modal-"+modalSize});
    } else {
      this.modalRef = this.modalService.show(template, {"animated": true});
    }
  }

  closeModal(modalId?: number): void{
    this.modalService.hide(modalId);
  }

  onAddRoutine(): void {
    this.postRoutine = true;
    this.emptyCommands.forEach(command => this.emptyRoutine.commands.push(command.toJson()))
    this.backendService.createRoutine(this.emptyRoutine).subscribe((routine) => {
      this.routines.push(routine);
      this.postRoutine = false;
      this.closeModal()
    });

    this.emptyRoutine = {name:"", description:"", onCommands:[], monday:false, tuesday:false, wednesday:false, thursday:false, friday:false, saturday:false, sunday:false, dateOfDay:[], clock_time:[], after_alarm:false, after_sunrise:false, after_sunset:false, after_call:false, commands:[]}
  }

  onAddTimeToEmptyRoutine(): void {
    this.emptyRoutine.clock_time.push(new Date());
  }

  onAddDateToEmptyRoutine(): void {
    this.emptyRoutine.dateOfDay.push(new Date());
  }

  onEmptyRoutineDateChange(event: any): void {

  }

  onEmptyRoutineTimeChange(event: any): void {

  }

  onEmptyTimeDelete(event: any): void {

  }

  onEmptyRepeatChange(king: string, event: any): void {

  }

  onAddCommandToEmptyRoutine(): void {
    this.emptyCommands.push(new Command(this.emptyCommands.length, "", []));
  }

  onChangeCommandOfEmptyRoutine(id: number, moduleName: string): void {
    let index: number = this.emptyCommands.findIndex(item => {
      return item.id === id;
    });

    this.emptyCommands[index].moduleName = moduleName;
  }

  onDeleteCommandOfEmptyRoutine(id: number): void {
    let index: number = this.emptyCommands.findIndex(item => {
      return item.id === id;
    });

    this.emptyCommands.splice(index, 1);
  }

  onDiscardRoutine(): void {
    this.emptyRoutine = {name:"", description:"", onCommands:[], monday:false, tuesday:false, wednesday:false, thursday:false, friday:false, saturday:false, sunday:false, dateOfDay:[], clock_time:[], after_alarm:false, after_sunrise:false, after_sunset:false, after_call:false, commands:[]}
  }

}
