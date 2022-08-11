import {JsonObject} from "@angular/compiler-cli/ngcc/src/packages/entry_point";

export class Command {
  id: number;
  moduleName: string;
  text: string[];

  constructor(id: number, moduleName: string, text: string[]) {
    this.id = id;
    this.moduleName = moduleName;
    this.text = text;
  }

  toJson(): JsonObject {
    return {
      "module_name": this.moduleName,
      "text": this.text
    }
  }
}
