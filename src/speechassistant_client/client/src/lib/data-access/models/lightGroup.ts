import {Light} from "./light";

export interface LightGroup {
  id: number;
  name: string;
  lights: Light[];
}
