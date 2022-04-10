import {Component, EventEmitter, HostBinding, Input, Output} from "@angular/core";

@Component({
  selector: 'tile-selector',
  templateUrl: './tileSelector.component.html',
  styleUrls: ['./tileSelector.component.scss']
})
export class TileSelectorComponent {
    @Input() text: string = "";
    @Input() checked: boolean = false;
    @Input() @HostBinding("style.--height") height: number = 100;
    @Output() onCheckedEvent = new EventEmitter<boolean>();



    onSateChanged(): void {
        this.checked = !this.checked;
    }

    getChecked(): boolean {
        return this.checked;
    }
}
