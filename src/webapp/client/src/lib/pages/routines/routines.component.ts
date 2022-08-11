import {Component, Input, OnInit, TemplateRef} from "@angular/core";
import {Routine} from "../../data-access/models";
import {BsModalRef, BsModalService} from 'ngx-bootstrap/modal';
import {Command} from "../../data-access/models/command";
import {RoutineStore} from "../../data-access/service/store/routine.store";
import {ModuleStore} from "../../data-access/service/store/module.store";

@Component({
  selector: 'routines',
  templateUrl: './routines.component.html',
  styleUrls: ['./routines.component.scss']
})
export class RoutinesComponent implements OnInit {

  title: string = "Routinen";
  emptyRoutine: Routine = {
    name: "",
    description: "",
    onCommands: [],
    monday: false,
    tuesday: false,
    wednesday: false,
    thursday: false,
    friday: false,
    saturday: false,
    sunday: false,
    dateOfDay: [],
    clock_time: [],
    after_alarm: false,
    after_sunrise: false,
    after_sunset: false,
    after_call: false,
    commands: []
  }
  emptyCommands: Command[] = [];
  modalRef?: BsModalRef;
  postRoutine: boolean = false;
  moduleNames: string[] = [];
  lastFocusedItemIndex: number = -1;


  @Input() routines: Routine[] = [];

  constructor(private modalService: BsModalService,
              private routineService: RoutineStore,
              private moduleStore: ModuleStore) {
  }

  ngOnInit(): void {
    this.routineService.loadRoutines().subscribe(routines => this.routines = routines);
    this.moduleStore.loadModuleNames().subscribe(moduleNames => {
      this.moduleNames = moduleNames;
    });
  }

  openModal(template: TemplateRef<any>, modalSize: string = ""): void {
    if (modalSize != "") {
      this.modalRef = this.modalService.show(template, {"animated": true, "class": "modal-" + modalSize});
    } else {
      this.modalRef = this.modalService.show(template, {"animated": true});
    }
  }

  closeModal(modalId?: number): void {
    this.modalService.hide(modalId);
  }

  getIndexOfTimeOfEmptyRoutine(time: Date): number {
    return this.emptyRoutine.clock_time.findIndex(t => t.getTime() == time.getTime());
  }

  onAddRoutine(): void {
    this.postRoutine = true;
    this.emptyCommands.forEach(command => this.emptyRoutine.commands.push(command.toJson()))
    this.routineService.addRoutine(this.emptyRoutine).subscribe(routines => this.routines = routines);

    this.postRoutine = false;
    this.closeModal()

    this.emptyRoutine = {
      name: "",
      description: "",
      onCommands: [],
      monday: false,
      tuesday: false,
      wednesday: false,
      thursday: false,
      friday: false,
      saturday: false,
      sunday: false,
      dateOfDay: [],
      clock_time: [],
      after_alarm: false,
      after_sunrise: false,
      after_sunset: false,
      after_call: false,
      commands: []
    }
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

  onAddTextToCommandOnEmptyRoutine(id: number): void {
    this.emptyCommands[id].text.push("");
  }

  onChangeTextOfCommandOnEmptyRoutine(id: number, newValue: string): void {
    this.emptyCommands[id].text[this.lastFocusedItemIndex] = newValue;
  }

  onChangeCommandOfEmptyRoutine(id: number, moduleName: string): void {
    let index: number = this.emptyCommands.findIndex(item => {
      return item.id === id;
    });

    this.emptyCommands[index].moduleName = moduleName;
  }

  updateFocusedIndex(id: number, value: string): void {
    this.lastFocusedItemIndex = this.emptyCommands[id].text.findIndex(t => t == value);
  }

  onDeleteCommandOfEmptyRoutine(id: number): void {
    let index: number = this.emptyCommands.findIndex(item => {
      return item.id === id;
    });

    this.emptyCommands.splice(index, 1);
  }

  onDiscardRoutine(): void {
    this.emptyRoutine = {
      name: "",
      description: "",
      onCommands: [],
      monday: false,
      tuesday: false,
      wednesday: false,
      thursday: false,
      friday: false,
      saturday: false,
      sunday: false,
      dateOfDay: [],
      clock_time: [],
      after_alarm: false,
      after_sunrise: false,
      after_sunset: false,
      after_call: false,
      commands: []
    }
  }

}
