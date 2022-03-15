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
