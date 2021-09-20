# Documentation

## local_storage
| Funktion | Beschreibung |
| ------------------ | ------------------ |
| "home_location" | **Type:** String<br/>Name der Stadt, in der sich der Sprachassistent befindet |
| "users" | **Type:** List<br/>Liste aller Nutzer. Diese beinhaltet die user_storages. |
| "messenger_allowed_id_table" | **Type:** Array<br/>Beinhaltet alle Telegram-Nutzer-IDs, welche mit dem Sprachassistenten kommunizieren dürfen. |
| "rejected_messenger_messages" | **Type:** Array<br/>Liste aller Nachrichten, die von nicht zugelassenen Telegram-Nutzern kamen. |
| "module_storage" | [Siehe in der Sektion des module_storage](###module_storage)|

### module_storage
| Funktion | | Beschreibung |
| ------------------ | ------------------ | ------------------ |
| "philips_hue": | "Bridge-Ip" | **Parametertyp:** String<br/>Enthält die IP der Bridge des Philips-Systems |
| "philips-tv": | | Weitere Informationen können in der [Doku von pylips](https://github.com/eslavnov/pylips) gefunden werden |
| | "user" | **Parametertyp:** String<br/>Enthält den Nutzernamen des Philips-TVs Nutzers |
| | "pass" | **Parametertyp:** String<br/>Enthält das Password des Philips-TVs Nutzers |
| | "host" | **Parametertyp:** String<br/>Enthält die IP-Adresse des Philips-TVs |

## Audio
### Audio-Input
| Funktion | Beschreibung |
| ------------------ | ------------------ |
| def recognize_file(audio_file) | transcribiert die übergebene Datei in String-Text |
| def recognize_input(listen=False, play_bling_before_listen=False) | **return:** String<br/>**Parametertyp:** listen: Boolean, play_bling_before_listen: Boolean <br/>Ist `listen == True`, dann wird der Text zurückgegeben, andernfalls wird `core.hotword_detected()` mit dem Text aufgerufen|

### Audio-Output

| Funktion | Beschreibung |
| ------------------ | ------------------ |
| def say(text) | **Parametertyp**: String<br/>Gibt den übergebenen text als Sprache aus. Ausgabe folgt dem [FIFO-Prinzip](https://www.prologistik.com/logistik-lexikon/fifo-first-in-first-out/)|
| def detected_hotword() | <b><font color="red">Nutze diese Funktion nur, wenn du weißt was du sie auch wirklich benötigst</font></b><br/>Die Funktion reguliert die Lautstärke der Ausgabe, damit die Spracheingabe besser verstanden werden kann und der Nutzer nicht irritiert wird. Dies erfolgt aber eigentlich immer Intern.|
 def continue_after_hotword() | <b><font color="red">Nutze diese Funktion nur, wenn du weißt was du sie auch wirklich benötigst</font></b><br/>Die Funktion setzt die Lautstärke wieder auf das "normale" Level zurück. Sie ist logisch immer nach einem `detect_hotword()` notwendig und auch logisch **nur** danach! |
 | def stop_notification() | Beendet die Ausgabe des aktuellen Elements der "notifications" |
 | def stop_music() | Beendet die Ausgabe des aktuellen Songs |
 | def stop_playback() | Beendet die Ausgabe des aktuellen Elements der "Playbacks" |
 

#### Möglichkeiten Audio abzuspielen
| Funktion | Beschreibung |
| ------------------ | ------------------ |
| def play_music(name, next=False) | **Parametertyp:** name: String, next: Boolean [OPTIONAL] <br/>Spiele **Musik**(-Titel)|
| def play_playback(buff, next) | **Parametertyp:** buff: Unbekannt, next: Boolean <br/>Spiele Sounds im Hintergrund|
| def play_notification(buff, next) | **Parametertyp:** buff: Unbekannt, next: Boolean <br/>Spiel ein wichtiges Geräusch oder Klang oder Sound|
| play_bling_sound() | Spielt ein Signalton zur Signalisierung, dass das System anschließend auf eine Spracheingabe des Nutzers hört. |

**Unterschied zwischen Funktionen**
<br/>Bei `play_music()` wird intern eine eigene Klasse verwendet. Diese sucht auch anhand des Songnamens den Titel im Internet heraus. `play_notification()` ist eine wichtige Ausgabe und wird intern gleichgestellt mit der Sprachausgabe. Möchte man zum Beispiel dem Nutzer etwas mitteilen, wie die Tagesthemen, ist dies ja eine informelle Ausgabe und wichtiger als zum Beispiel ein Lied im Hintergrund. Alles was nichts mit Musik aber auch nicht mit einer wichtigen/informellen Ausgabe zu tun hat, wird über `play_playback()` geregelt. Das können zum Beispiel Hintergrundgeräusche sein, die bei einer Sprachausgabe pausiert werden sollen.

## Zusatzfunktionen
### wartende Benachrichtigungen

jeder Nutzer hat in seiner .json einen Parameter namens `wartende_benachrichtigungen`.
Diese werden nach jedem Aufruf eines Nutzer abbgefragt und ausgegeben, falls etwas ansteht.
Beginnt man eine Benachrichtigung mit `\Audio:` wird der anschließende Teil des Strings als Pfad interpretiert und als Audio abgespielt.

um eine neue Benachrichtigung hinzuzufügen benutzt man folgende Syntax: <br/>
`String message = "|OPTIONAL: \Audio:|Nachricht oder Pfad"`<br/>
`core.local_storage["users"][NUTZERNAME].append({"message": message, "Date":|OPTIONAL: datetime.datetime.date|})`

### Module Skills
| Funktion | Anwendung |
| ------------------ | ------------------ |
| def get_enumerate(array) | **return**: String <br/>**Parametertyp**: array <br/>Aus ["Apfel", "Birne", " Banane ", "Gurke"] wird "Apfel, Birne, Banane **und** Gurke"|
| def is_approved(text)  | **return**: boolean <br/>**Parametertyp**: String <br/>Gibt True zurück, wenn der Nutzer die einen willenden Ausdruck macht, sonst False|
| def get_text_beetween(start_word, text) | **return**: array / String <br/>**Parametertyp**:<br/>- start_word: String <br/>- text: String<br/> **optionale Parameter:**<br/>- end_word: <br/>Wid ein Endword angegeben (`get_text_beetween("erstes", "", end_word="bis"`), geht der Teilstring nur bis zum Word end_word<br/>- **output**: Etnweder array oder String. Der jeweilige parameter bestimmt den Typ des Rückgabewertes<br/>- **split_text** Wenn True wird der Text bei jedem Leerzeichen getrennt. Anwendung unbekannt.|
|def delete_duplications(array)| <h3><font color="red">**Work in Progress**</font></h3>**return:** array <br/>**Parametertyp:** array <br/>Aus `["Apfel", "Birne", "Apfel", "Banane"]` wird `["Apfel", "Birne", "Banane"]`|
|def assamble_new_items(array1, array2)| **return:** array<br/>**Parametertyp:** array1/2: array<br/>Aus `["Apfel", "Birne", "Butter", "2 Milch", "250g Rinderhack"]` und `["Zwiebel", "Apfel", "Milch", "1kg Rinderhack"]` wird `["2 Apfel, "Birne", "Butter", "3 Milch", "Zwiebel, "1250g Rinderhack"]`|
|def is_enthalten(item, array) | **return:** boolean<br/>**Parametertyp:** <br/>- item: String <br/>- array: array|
|def get_value_number(item)| **return:** <br/>- value: String<br/>- number: int<br/>**Parametertyp:** String<br/>Es werden Zahl und Einheit voneinander getrennt und einzeln zurückgegeben.<br/>Dabei wird aus<br/>- kg -> g<br/>|
|def get_time(i) | **return:** String<br/>**Parametertyp:** datetime-Object<br/>Wandelt ein Datetime-Object in eine textuelle Form um|
|def is_desired(text) | **return:** boolean<br/>**Parametertyp:** String<br/>Gibt als boolean zurück, ob im Text ein Ausdruck des Wollens vorkommt:<br/>Ja bitte! -> return true<br/>gerne -> return true<br/>nein, danke! -> return false|
| class Statistics | Hier sind staitsche Werte häufig als Map oder Array gespeichert. <br/>Derzeit sind folgende Punkte vorhanden: <br/> - **color_ger_to_eng:** "blau"->"blue", "rot"->"red"<br/> - **color_eng_to_ger:** "blue"->"blau", "red"->"rot"<br/> - **weekdays:** `["Montag", "Dienstag", ...]`<br/> - **weekdays_engl:** `["Monday", "Tuesday", ...]`<br/> - **weekdays_ger_to_eng:** "montag"->"monday", "dienstag"->"tuesday"<br/>**weekdays_eng_to_ger:** "monday"->"montag", "tuesday"->"dienstag"<br/>**numb_to_day:** "1"->"monday", "2"->"dienstag"

## Webserver
### Websites

| Extension | Beschreibung |
| ------------------ | ------------------ |
| /index | Mainpage |
| /devIndex | Mainpage mit paar mehr Informationen zum System |
| /setup | Einrichtungsassistent |
| /setupSystem | Einrichtungsassistent für das System |
| /setupUser | Einrichtungsassistent für Nutzer |
| /phue | Übersicht über alle Philips HUE Lampen |
| /alarm | Übersicht über alle Wecker mit Bearbeitungsfunktionen |
| /weatherOverview | Wettervorhersage |
| /editModule/`moduleName` | Bearbeitungs GUI für ein bestimmtes Modul |

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
| /api/alarm/delete/`repeat`/`day`/`hour`/`minute` | löscht den >repeat< Wecker an dem `day` um >hour< <b>:</b> `minute` Uhr |
| /api/alarm/create/`repeat`/`day`/`hour`/`minute` | erstellt einen >repeat< Wecker an dem `day` um `hour` <b>:</b> `minute` Uhr |
