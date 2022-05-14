
import {Component, Input, OnInit, TemplateRef} from "@angular/core";
import { Routine } from "../../data-access/models";
import {BackendService} from "../../data-access/service/backend.service";
import { BsModalService, BsModalRef } from 'ngx-bootstrap/modal';
import {Command} from "../../data-access/models/command";
import {materialModuleSpecifier} from "@angular/material/schematics/ng-update/typescript/module-specifiers";
import {retry} from "rxjs";
import {RoutineStore} from "../../data-access/service/store/routine.store";

@Component({
  selector: 'routines',
  templateUrl: './routines.component.html',
  styleUrls: ['./routines.component.scss']
})
export class RoutinesComponent implements OnInit{

  title: string = "Routinen";
  emptyRoutine: Routine = { name:"", description:"", onCommands:[], monday:false, tuesday:false, wednesday:false, thursday:false, friday:false, saturday:false, sunday:false, dateOfDay:[], clock_time:[], after_alarm:false, after_sunrise:false, after_sunset:false, after_call:false, commands:[] }
  emptyCommands: Command[] = [];
  modalRef?: BsModalRef;
  postRoutine: boolean = false;
  moduleNames: string[] = [];

  @Input() routines: Routine[] = [];

  constructor(private modalService: BsModalService,
              private routineService: RoutineStore) { }

  ngOnInit(): void {
    this.routineService.loadAndGetRoutines().subscribe( routines => this.routines = routines );
  }

}
