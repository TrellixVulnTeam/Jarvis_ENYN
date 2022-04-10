export class OnCommand {
    id: number;
    text: string;

    constructor(id: number, text: string) {
        this.id = id;
        this.text = text;
    }

    getID(): number {
      return this.id;
    }

    getText(): string {
      return this.text;
    }

    setText(givenText: string): void {
        this.text = givenText;
    }
}
