### Audio-Input
| Funktion | Beschreibung |
| ------------------ | ------------------ |
| def recognize_file(audio_file) | transcribiert die übergebene Datei in String-Text |
| def recognize_input(listen=False, play_bling_before_listen=False) | **return:** String<br/>**Parametertyp:** listen: Boolean, play_bling_before_listen: Boolean <br/>Ist `listen == True`, dann wird der Text zurückgegeben, andernfalls wird `core.hotword_detected()` mit dem Text aufgerufen|
