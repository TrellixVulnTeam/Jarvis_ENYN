## local_storage
| Funktion | Beschreibung                                                                                                   |
| ------------------ |----------------------------------------------------------------------------------------------------------------|
| "home_location" | **Type:** String<br/>Name der Stadt, in der sich der Sprachassistent befindet                                  |
| "users" | **Type:** List<br/>Liste aller Nutzer. Diese beinhaltet die user_storages.                                     |
| "messenger_allowed_id_table" | **Type:** Array<br/>Beinhaltet alle Telegram-Nutzer-IDs, welche mit dem Sprachassistenten kommunizieren dürfen. |
| "rejected_messenger_messages" | **Type:** Array<br/>Liste aller Nachrichten, die von nicht zugelassenen Telegram-Nutzern kamen.                |
| "module_storage" | [Siehe in der Sektion des module_storage](###module_storage)                                                   |

###module_storage
| Funktion | | Beschreibung |
| ------------------ | ------------------ | ------------------ |
| "philips_hue": | "Bridge-Ip" | **Parametertyp:** String<br/>Enthält die IP der Bridge des Philips-Systems |
| "philips-tv": | | Weitere Informationen können in der [Doku von pylips](https://github.com/eslavnov/pylips) gefunden werden |
| | "user" | **Parametertyp:** String<br/>Enthält den Nutzernamen des Philips-TVs Nutzers |
| | "pass" | **Parametertyp:** String<br/>Enthält das Password des Philips-TVs Nutzers |
| | "host" | **Parametertyp:** String<br/>Enthält die IP-Adresse des Philips-TVs |