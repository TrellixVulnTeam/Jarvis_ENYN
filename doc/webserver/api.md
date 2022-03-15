
### /api
| Extension | Beschreibung |
| ------------------ | ------------------ |
| /api/installer/listPackages |  |
| /api/writeConfig/system | **getData()** required<br/>Überschreibt alle gesetzten Parameter in den Configs.  |
| /api/writeConfig/user/`userName` | **getData()** required<br/>Überschreibt alle gesetzten Parameter in den Configs des gewählten Users. |
| /api/loadConfig/user/`userName` | **returnt:** User Configs des gewählten Users. |
| /api/loadConfig/server/list/`action` | -users<br/>-modules<br/>-telegram<br/>-externSystems<br/>-alarmSounds|
|||
| /api/module /`moduleName`/`action` | **Voraussetzung:** moduleName muss in der Modul-Liste aus dem Local_Storage enthalten sein<br/>**action-Möglichkeiten:** <br/>-load<br/>-unload<br/>-status<br/>-update |
|||
| /api/phue/change/color/`name`/`value` | Ändert die Farbe des Lichts mit dem `name` in den `value` |
| /api/phue/change/powerState/`name`/`value` | Schalte Licht mit dem Namen `name` an/aus |
| /api/phue/change/brightness/`name`/`value` | Änder die Helligkeits des Lichts mit dem `name` und `value` als Wert|
| /api/phue/createGroup/`name` | **getData()** required<br/>Erstelle eine neue Gruppe mit `name` als Name und den Lichtern aus getData() |
| /api/phue/renameGroup/`name`/`value` | rename Group with name `name` to `value` |
| /api/phue/changeLightsInGroup/`name` | **getData()** required<br/> änder Lichter in einer Gruppe in getData() |
| /api/phue/list/lights | gibt alle Lichter zurück. <br/>Format: [{"id", "name", "on", "brightness", "color", "saturation"}]|
| /api/phue/list/light/`name` |gibt die Informationen eines Lichts zurück. <br/>Format: {"on", "brightness", "name"} |
| /api/phue/list/groups | gibt alle Gruppen zurück. <br/>Format: siehe [phue](https://github.com/studioimaginaire/phue/blob/master/README.md) |
| /api/phue/list/group/`name` | gibt die Informationen zu der Guppe mit dem `name` zurück. <br/>Format: siehe [phue](https://github.com/studioimaginaire/phue/blob/master/README.md)|
|||
| /api/alarm/getSound/`filename` | gibt den Ton des Alarm-Sounds mit dem Namen `filename` zurück |
| /api/alarm/list/alarms | Gibt alle Wecker zurück. <br/>Format: {"regular_alarm": List, "single_alarm": List, "singlePresent": Boolean, "regularPresent": Boolean} |
| /api/alarm/isPresent | Gibt zurück, ob reguläre und einzelne Wecker gestellt sind <br/>Format: {"single", "regular"} |
| /api/alarm/alarmSounds | Gibt alle AlarmSounds zurück.<br/>Format: {"alarmSounds": Array}
| /api/alarm/delete/`repeat`/`day`/`hour`/`minute` | löscht den `repeat` Wecker an dem `day` um `hour` <b>:</b> `minute` Uhr |
| /api/alarm/create/`repeat`/`day`/`hour`/`minute` | erstellt einen `repeat` Wecker an dem `day` um `hour` <b>:</b> `minute` Uhr |
