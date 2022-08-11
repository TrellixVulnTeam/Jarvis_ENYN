import {Component, Input, OnInit, TemplateRef, ViewChild} from "@angular/core";
import {Alarm} from "../../data-access/models/alarm";
import {Title} from "@angular/platform-browser";
import {ActivatedRoute, Router} from "@angular/router";
import {BsModalRef, BsModalService} from "ngx-bootstrap/modal";
import {AlarmStore} from "../../data-access/service/store/alarm.store";
import {SoundStore} from "../../data-access/service/store/sound.store";

@Component({
  selector: 'alarm',
  templateUrl: './alarm.component.html',
  styleUrls: ['./alarm.component.scss']
})
export class AlarmComponent implements OnInit {

  // @ts-ignore
  @Input() alarm: Alarm;
  // @ts-ignore
  @ViewChild('alarmChangeRepeating') createRepeatModal: TemplateRef<any>;
  // @ts-ignore
  @ViewChild('alarmChangeText') createTextModal: TemplateRef<any>;

  repeatingModalRef?: BsModalRef;
  textModalRef?: BsModalRef;
  soundNames: string[] = ['standard', 'test'];

  constructor(private alarmStore: AlarmStore,
              private soundStore: SoundStore,
              private titleService: Title,
              private activatedRoute: ActivatedRoute,
              private route: Router,
              private modalService: BsModalService) {
  }

  ngOnInit() {
    this.titleService.setTitle('Wecker');
    this.activatedRoute.params.subscribe(params => {
      this.alarmStore.getAlarm(params['id']).subscribe(alarm => {
        this.alarm = alarm;
      });
    });
    this.soundStore.loadSoundNames().subscribe(names => {
      this.soundNames = names;
    });
  }

  onDeleteAlarm(): void {
    if (this.alarm.id != null) {
      this.alarmStore.deleteAlarm(this.alarm.id);
    }
    this.route.navigate(['/alarms'])
  }

  onChangeRepeating(): void {
    this.alarmStore.updateAlarm(this.alarm);
  }

  onChangeText(value: string): void {
    this.alarm.text = value;
    this.alarmStore.updateAlarm(this.alarm);
  }

  onChangeSound(): void {
    this.alarmStore.updateAlarm(this.alarm);
  }


  openRepeatingModal(): void {
    this.repeatingModalRef = this.modalService.show(this.createRepeatModal);
  }

  openTextModal(): void {
    this.textModalRef = this.modalService.show(this.createTextModal);
  }

  closeRepeatingModal(): void {
    this.modalService.hide(this.repeatingModalRef?.id);
  }

  closeTextModal(): void {
    this.modalService.hide(this.textModalRef?.id);
  }

  closeAllModals(): void {
    this.modalService.hide(this.repeatingModalRef?.id);
    this.modalService.hide(this.textModalRef?.id);
  }

  rtrim(input: string, characters: string): string {
    let start = 0;
    let end = input.length - 1;
    while (characters.indexOf(input[end]) >= 0) {
      end -= 1;
    }
    return input.substr(0, end + 1);
  }
}
