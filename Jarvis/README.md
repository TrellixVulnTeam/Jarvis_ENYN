# Documentation

## Zusatzfunktionen

### wartende Benachrichtigungen

jeder Nutzer hat in seiner .json einen Parameter namens `wartende_benachrichtigungen`. Diese werden nach jedem Aufruf
eines Nutzer abbgefragt und ausgegeben, falls etwas ansteht. Beginnt man eine Benachrichtigung mit `\Audio:` wird der
anschließende Teil des Strings als Pfad interpretiert und als Audio abgespielt.

um eine neue Benachrichtigung hinzuzufügen benutzt man folgende Syntax:
`String message = "|OPTIONAL: \Audio:|Nachricht oder Pfad"
core.local_storage["users"][NUTZERNAME].append({"message": message, "Date":|OPTIONAL: datetime.datetime.date|})`

### Module Skills

| Funktion | Anwendung |
| ------------------ | ------------------ |
| def get_enumerate(array) | return: String <br/>Aus ["Apfel", "Birne", " Banane ", "Gurke"] wird "Apfel, Birne, Banane **
und** Gurke"|
| def is_approved(text)  | return: boolean <br/>Gibt True zurück, wenn der Nutzer die einen willenden Ausdruck macht, sonst False|
| def get_text_beetween(start_word, text) | return: array / String <br/> <h5>optionale Parameter:</h5>- **
end_word**: <br/>Wid ein Endword angegeben (`get_text_beetween("erstes", "", end_word="bis"`), geht der Teilstring nur bis zum Word end_word<br/><h5>-output:</h5>Etnweder `array` oder `String`. Der jeweilige parameter bestimmt den Typ des Rückgabewertes<br/><h5>- split_text</h5>Wenn True wird der Text bei jedem Leerzeichen getrennt. Anwendung unbekannt.

