import logging
import re
from src.speechassistant.core import ModuleWrapper
from src.speechassistant.resources.module_skills import Skills

"""
class ModuleWrapper:
    def __init__(self):
        self.local_storage = {"shopping_list": {}}
        self.messenger_call = False

    def say(self, text: str) -> None:
        print(text)

    def listen(self, text: str = None) -> str:
        if text is not None: print(text)
        return input(text)


class Skills:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_enumerate(array: list):
        new_array = []
        for item in array:
            new_array.append(item.strip(' '))

        ausgabe = ''
        if len(new_array) == 0:
            pass
        elif len(new_array) == 1:
            ausgabe = array[0]
        else:
            for item in range(len(new_array) - 1):
                ausgabe += new_array[item] + ', '
            ausgabe = ausgabe.rsplit(', ', 1)[0]
            ausgabe = ausgabe + ' und ' + new_array[-1]
        return ausgabe
"""

def prepare_text(text: str) -> str:
    # The text is split only at "and".
    text = text.replace(' Und ', ' und ')
    # calculate_units() works with the abbreviations
    text = text.replace(' g ', 'g ')
    text = text.replace(' gram ', 'g ')
    text = text.replace(' kg ', 'kg ')
    text = text.replace(' kilogram ', 'kg ')
    # "ein", etc are superfluous and can only lead to errors
    text = text.replace('eine ', '')
    text = text.replace('einen ', '')
    text = text.replace('ein ', '')
    return text


def get_items(text: str) -> list:
    return text.split(' und ')


def get_shopping_list(shopping_list: dict, skills: Skills, for_messenger: bool = False) -> str:
    anz_items = len(shopping_list.keys())
    if anz_items == 0:
        return 'Aktuelle hast du keine Artikel auf deiner Einkaufsliste.'

    response = "Du hast aktuell "
    if anz_items == 1:
        response += 'nur '
    item_list = []

    # if the output is for the messenger, there should be a TAB between the quantity and the name, otherwise a SPACE
    if for_messenger:
        space = '\t'
    else:
        space = ' '
    for item in shopping_list.keys():
        item_list.append(simplify_unit(shopping_list.get(item)) + space + shopping_list.get(item)['name'])

    # remove the ',' after the last item and return
    if for_messenger:
        response += '\n'
        for item in item_list:
            response += '\t' + item + ', \n'
        return response[0:len(response) - 3] + '\n' + 'auf deiner Einkaufsliste.'
    else:
        return response + skills.get_enumerate(item_list) + ' auf deiner Einkaufsliste.'


def simplify_unit(item: dict) -> str:
    if item.get('measure') == 'g' and item.get('quantity') >= 1000:
        return str(item.get('quantity') / 1000) + 'kg'

    elif item.get('measure') == 'ml' and item.get('quantity') >= 1000:
        return str(item.get('quantity') / 1000) + 'l'

    else:
        return str(item.get('quantity')) + item.get('measure')


def dlt_items(text: str, core: ModuleWrapper) -> list:
    text = text.lower()
    del_items = []
    # search for items to be deleted from text
    for item in core.data_base.shoppinglist_interface.get_list():
        if item['name'].lower() in text:
            del_items.append(item)
    # delete items
    for item in del_items:
        core.data_base.shoppinglist_interface.remove_item(item)

    return del_items


def calculate_units(items: list) -> list[dict]:
    new_items = []
    for item in items:
        potential_measure = item.split(' ')[0].replace(',', '.')

        # if the item consists of more than one word, the first could be the unit and the rest the name
        temp_split = item.split(' ', 1)
        if len(temp_split) > 1:
            potential_name = temp_split[1]
        else:
            potential_name = item

        # convert the individual units into the smallest unit (l -> ml; kg -> g)
        current_item = {'measure': '', 'quantity': 0.0, 'name': ''}
        if re.match("\d+(\.\d+)?kg", potential_measure):
            current_item['measure'] = 'g'
            current_item['quantity'] = float(potential_measure.replace('kg', '')) * 1000
            current_item['name'] = potential_name
        elif re.match("\d+(\.\d+)?g", potential_measure):
            current_item['measure'] = 'g'
            current_item['quantity'] = float(potential_measure.replace('g', ''))
            current_item['name'] = potential_name
        elif re.match("\d+(\.\d+)?ml", potential_measure):
            current_item['measure'] = 'ml'
            current_item['quantity'] = float(potential_measure.replace('ml', ''))
            current_item['name'] = potential_name
        elif re.match("\d+(\.\d+)?l", potential_measure):
            current_item['measure'] = 'ml'
            current_item['quantity'] = float(potential_measure.replace('ml', '')) * 1000
            current_item['name'] = potential_name
        elif is_float(potential_measure):
            current_item['quantity'] = potential_measure
            current_item['name'] = potential_name
        else:
            current_item['name'] = item
            current_item['quantity'] = 1
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
    if 'setz' in lower_text or 'schreib' in lower_text:
        text = text.replace('Setz ', '')
        text = text.replace('setz', '')
        text = text.replace(' auf die Einkaufsliste', '')
        new_items = calculate_units(get_items(text))
        for item in new_items:
            item_name = item.get('name')
            if core.data_base.shoppinglist_interface.is_item_in_list(item_name):
                shopping_list.get(item_name)['quantity'] += item.get('quantity')
            else:
                core.data_base.shoppinglist_interface.add_item(item.get('name'), item.get('measure'), item.get('quantity'))
    elif ('was' in lower_text and 'steht' in lower_text) or ('gib' in lower_text and 'aus' in lower_text):
        core.say(get_shopping_list(shopping_list, skills, for_messenger=core.messenger_call))
    elif 'lösch' in lower_text or 'entfern' in lower_text:
        if len(shopping_list) == 0:
            core.say(['Deine Einkaufsliste ist bereits leer.', 'Ich kann das nicht aus deiner Einkaufsliste löschen, da sie leer ist.'])
        else:
            deleted_items = dlt_items(text, core)
            if len(deleted_items) == 0:
                core.say(deleted_items[0].get('name') + ' wurde [|erfolgreich] von der Einkaufsliste entfernt.')
            else:
                core.say(skills.get_enumerate(deleted_items) + ' wurden [|erfolgreich] von der Einkaufsliste entfernt.')


if __name__ == "__main__":

    core = ModuleWrapper()
    skills = Skills()

    """
    print(simplify_unit({'measure': 'g', 'quantity': 10}))
    print(simplify_unit({'measure': 'g', 'quantity': 1500}))
    print(simplify_unit({'measure': 'kg', 'quantity': 10}))
    print(simplify_unit({'measure': 'ml', 'quantity': 10}))
    print(simplify_unit({'measure': 'ml', 'quantity': 10000}))
    """

    handle("Was steht auf meiner Einkaufsliste?", core, skills)
    handle("Setz Butter und Milch und 150g Rinderhack auf die Einkaufsliste", core, skills)
    handle("Was steht auf meiner Einkaufsliste?", core, skills)
    handle("Setz 2 Bananen und 150ml Rinderbrühe und Milch auf die Einkaufsliste", core, skills)
    handle("Setz 1.5kg Rinderhack auf die Einkaufsliste", core, skills)
    handle("Was steht auf meiner Einkaufsliste?", core, skills)
    handle("Lösch Rinderbrühe von meiner Einkaufsliste", core, skills)
    handle("Was steht auf meiner Einkaufsliste?", core, skills)
    # print(calculate_units(['500g Mehl', 'Bananen', 'Zwiebeln']))
