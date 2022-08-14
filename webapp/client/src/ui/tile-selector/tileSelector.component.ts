import {Component, EventEmitter, Input, Output} from "@angular/core";

@Component({
  selector: 'tile-selector',
  templateUrl: './tileSelector.component.html',
  styleUrls: ['./tileSelector.component.scss']
})
export class TileSelectorComponent {

    // @ts-ignore
  @Input() text: string;
    // @ts-ignore
  @Input() checked: boolean;
    @Output() onCheckedEvent = new EventEmitter<boolean>();

    onSateChanged(): void {
        this.checked = !this.checked;
    }

    getChecked(): boolean {
        return this.checked;
    }
}
