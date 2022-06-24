import re
from core import ModuleWrapper
from resources.module_skills import Skills


def isValid(text):
    text = text.lower()
    if "to" in text and "do" in text and "liste" in text:
        return False
    if "einkaufsliste" in text:
        if (
            "setz" in text
            or "setzte" in text
            or "schreib" in text
            or "schreibe" in text
            or "füg" in text
            or "füge" in text
        ):
            return True
        elif ("was" in text and "steht" in text and "auf" in text) or (
            "gib" in text and "aus" in text
        ):
            return True
        elif ("lösch" in text or "leere" in text) and "einkaufsliste" in text:
            return True
        elif "send" in text or "schick" in text or "schreib" in text:
            return True
        elif "räum" in text and "auf" in text:
            return True
    else:
        return False


def prepare_text(text: str) -> str:
    # The text is split only at "and".
    text = text.replace(" Und ", " und ")
    # calculate_units() works with the abbreviations
    text = text.replace(" g ", "g ")
    text = text.replace(" gram ", "g ")
    text = text.replace(" kg ", "kg ")
    text = text.replace(" kilogram ", "kg ")
    # "ein", etc are superfluous and can only lead to errors
    text = text.replace(" eine ", "")
    text = text.replace(" einen ", "")
    text = text.replace(" ein ", "")
    return text


def get_items(text: str) -> list:
    return text.split(" und ")


def get_shopping_list(
    shopping_list: dict, skills: Skills, for_messenger: bool = False
) -> str:
    anz_items = len(shopping_list)
    if anz_items == 0:
        return "Aktuelle hast du keine Artikel auf deiner Einkaufsliste."

    response = "Du hast aktuell "
    if anz_items == 1:
        response += "nur "
    item_list = []

    # if the output is for the messenger, there should be a TAB between the quantity and the name, otherwise a SPACE
    if for_messenger:
        space = "\t"
    else:
        space = " "
    for item in shopping_list:
        item_list.append(simplify_unit(item) + space + item["name"])

    # remove the ',' after the last item and return
    if for_messenger:
        response += "\n"
        for item in item_list:
            response += "\t" + item + ", \n"
        return response[0 : len(response) - 3] + "\n" + "auf deiner Einkaufsliste."
    else:
        return response + skills.get_enumerate(item_list) + " auf deiner Einkaufsliste."


def simplify_unit(item: dict) -> str:
    if item.get("measure") == "g" and item.get("quantity") >= 1000:
        return str(item.get("quantity") / 1000) + "kg"

    elif item.get("measure") == "ml" and item.get("quantity") >= 1000:
        return str(item.get("quantity") / 1000) + "l"

    else:
        return str(item.get("quantity")) + item.get("measure")


def dlt_items(text: str, core: ModuleWrapper) -> list:
    text = text.lower()
    del_items = []
    # search for items to be deleted from text
    for item in core.data_base.shoppinglist_interface.get_list():
        if item["name"].lower() in text:
            del_items.append(item["name"])
    # delete items
    for item in del_items:
        core.data_base.shoppinglist_interface.remove_item(item)

    return del_items


def calculate_units(items: list) -> list[dict]:
    new_items = []
    for item in items:
        potential_measure = item.split(" ")[0].replace(",", ".")

        # if the item consists of more than one word, the first could be the unit and the rest the name
        temp_split = item.split(" ", 1)
        if len(temp_split) > 1:
            potential_name = temp_split[1]
        else:
            potential_name = item

        # convert the individual units into the smallest unit (l -> ml; kg -> g)
        current_item = {"measure": "", "quantity": 0.0, "name": ""}
        if re.match("\d+(\.\d+)?kg", potential_measure):
            current_item["measure"] = "g"
            current_item["quantity"] = float(potential_measure.replace("kg", "")) * 1000
            current_item["name"] = potential_name
        elif re.match("\d+(\.\d+)?g", potential_measure):
            current_item["measure"] = "g"
            current_item["quantity"] = float(potential_measure.replace("g", ""))
            current_item["name"] = potential_name
        elif re.match("\d+(\.\d+)?ml", potential_measure):
            current_item["measure"] = "ml"
            current_item["quantity"] = float(potential_measure.replace("ml", ""))
            current_item["name"] = potential_name
        elif re.match("\d+(\.\d+)?l", potential_measure):
            current_item["measure"] = "ml"
            current_item["quantity"] = float(potential_measure.replace("ml", "")) * 1000
            current_item["name"] = potential_name
        elif is_float(potential_measure):
            current_item["quantity"] = potential_measure
            current_item["name"] = potential_name
        else:
            current_item["name"] = item
            current_item["quantity"] = 1
        new_items.append(current_item)

    return new_items


def is_float(string: str) -> bool:
    if string == "":
        return False
    try:
        float(string)
        return True
    except ValueError:
        return False


def handle(text: str, core: ModuleWrapper, skills: Skills):
    text = prepare_text(text)
    lower_text = text.lower()
    shopping_list = core.data_base.shoppinglist_interface.get_list()
    if "setz" in lower_text or "schreib" in lower_text:
        text = text.replace("Setz ", "")
        text = text.replace("setz", "")
        text = text.replace(" auf die Einkaufsliste", "")
        new_items = calculate_units(get_items(text))
        for item in new_items:
            item_name = item.get("name")
            if core.data_base.shoppinglist_interface.is_item_in_list(item_name):
                new_quantity = core.data_base.shoppinglist_interface.get_item(
                    item_name
                ).get("quantity") + float(item.get("quantity"))
                core.data_base.shoppinglist_interface.update_item(
                    item_name, new_quantity
                )
            else:
                core.data_base.shoppinglist_interface.add_item(
                    item.get("name"), item.get("measure"), item.get("quantity")
                )
    elif ("was" in lower_text and "steht" in lower_text) or (
        "gib" in lower_text and "aus" in lower_text
    ):
        core.say(
            get_shopping_list(shopping_list, skills, for_messenger=core.messenger_call)
        )
    elif "lösch" in lower_text or "entfern" in lower_text:
        if len(shopping_list) == 0:
            core.say(
                [
                    "Deine Einkaufsliste ist bereits leer.",
                    "Ich kann das nicht aus deiner Einkaufsliste löschen, da sie leer ist.",
                ]
            )
        else:
            deleted_items: list = dlt_items(text, core)
            if len(deleted_items) == 1:
                core.say(
                    deleted_items[0]
                    + " wurde [|erfolgreich] von der Einkaufsliste entfernt."
                )
            else:
                core.say(
                    skills.get_enumerate(deleted_items)
                    + " wurden [|erfolgreich] von der Einkaufsliste entfernt."
                )
