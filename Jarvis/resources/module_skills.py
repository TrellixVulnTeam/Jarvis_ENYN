class skills:
    def __init__(self):
        pass

    @staticmethod
    def get_enumerate(array):
        # print(array)
        new_array = []  # array=['Apfel', 'Birne', 'Gemüse', 'wiederlich']
        for item in array:
            new_array.append(item.strip(' '))

        # print(new_array)
        ausgabe = ''
        # print('Länge: {}'.format(len(new_array)))
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

    @staticmethod
    def is_approved(text):
        if ('ja' in text or 'gerne' in text or 'bitte' in text) and not (
                'nein' in text or 'nicht' in text or 'nö' in text or 'ne' in text):
            return True
        else:
            return False

    @staticmethod
    def get_text_beetween(start_word, text, end_word='', output='array', split_text=True):
        ausgabe = []
        index = -1
        start_word = start_word.lower()
        text = text.replace(".", "")
        if split_text:
            text = text.split(' ')
        for i in range(len(text)):
            # Erst hier .lower um Groß- und Kleinschreibung beizubehalten
            if text[i].lower() == start_word:
                index = i + 1

        if index is not -1:
            if end_word == '':
                for i in range(index, len(text)):
                    ausgabe.append(text[i])
            else:
                founded = False
                while index <= len(text) and not founded:
                    if text[index] is end_word:
                        founded = True
                    else:
                        ausgabe.append(text[index])
                        index += 1
        if output is 'array':
            return ausgabe
        elif output is 'String':
            ausgabe_neu = ''
            for item in ausgabe:
                ausgabe_neu += item + ' '
            return ausgabe_neu

    @staticmethod
    def delete_duplications(array):
        return list(set(array))

    def assamble_new_items(self, array1, array2):
        new_array = []
        for item in array1:
            value1, number1 = self.get_value_number(item)
            try:
                item1 = item.split(" ", 1)[1].lower()
            except:
                item1 = item.lower()
            for field in array2:
                value2, number2 = self.get_value_number(field)
                try:
                    item2 = field.split(" ", 1)[1].lower()
                except:
                    item2 = field.lower()
                # print(f"value1: {item1}, {number1}, {value1};    value2: {item2}, {number2}, {value2}")
                if item1 == item2 or item1.rstrip(item1[-1]) == item2 or item1 == item2.rstrip(item2[-1]):
                    if item1[-1] == "e":
                        item1 += "n"
                    if value1 == value2:
                        final_value = value1
                        final_number = number1 + number2
                        if final_number >= 1000 and final_value == "g":
                            final_value = "kg"
                            final_number /= 1000
                    else:
                        final_value = ""
                        final_number = -1
                    if final_number != -1:
                        new_array.append(str(final_number) + final_value + " " + item1.capitalize())
                    else:
                        new_array.append(item1.capitalize())
                else:
                    if self.is_enthalten(item1, array2):
                        new_array.append(item1.capitalize())
                    if self.is_enthalten(item2, array1):
                        new_array.append(item2.capitalize())

        return self.delete_duplications(new_array)

    @staticmethod
    def is_enthalten(item, array):
        item = item.lower()
        valid = True
        for position in array:
            try:
                item_position = position.split(" ", 1)[1].lower()
            except:
                item_position = position.lower()
            if item_position == item or item_position.rstrip(item_position[-1]) == item or item_position == item.rstrip(
                    item[-1]):
                valid = False
        return valid

    @staticmethod
    def get_value_number(item):
        first_value = item.split(' ', 1)[0]
        value = ""
        number = -1
        if "kg" in first_value:
            try:
                first_value.replace("kg", "")
                value = "g"
                number = int(first_value) * 1000
            except:
                pass
        elif "g" in first_value:
            try:
                first_value1 = first_value.replace("g", "")
                value = "g"
                number = int(first_value1)
            except:
                pass
        elif "ml" in first_value:
            try:
                first_value = first_value.replace("ml", "")
                value = "ml"
                number = int(first_value)
            except:
                pass
        else:
            try:
                number = int(first_value)
            except:
                pass
        return value, number

    def assamble_array(self, array):
        # print(f"Beim Start von assamble_array: {array}")
        temp_array = []
        temp_array0 = array
        for item in temp_array0:
            item = item.replace('1', '')
            item = item.replace('2', '')
            item = item.replace('3', '')
            item = item.replace('4', '')
            item = item.replace('5', '')
            item = item.replace('6', '')
            item = item.replace('7', '')
            item = item.replace('8', '')
            item = item.replace('9', '')
            item = item.replace('0', '')
            item = item.strip()
            temp_array.append(item)
        duplications = self.delete_duplications(temp_array)
        temp3_array = []
        if len(duplications) >= 1:
            temp2_array = self.assamble_new_items(array, duplications)
            for item in temp2_array:
                try:
                    anz = int(item.split(' ', 1)[0])
                except:
                    anz = 1
                anz -= 1

                if anz == 1:
                    item = item.split(' ')[1]
                else:
                    item = str(anz) + " " + item.split(' ', 1)[1]
                temp3_array.append(item)

        return temp3_array

    def get_time(self, i):
        try:
            hour = i["hour"]
        except:
            hour = i.hour
        try:
            minute = i["minute"]
        except:
            minute = i.minute
        next_hour = hour + 1
        if next_hour == 24:
            next_hour = 0
        hour = str(hour) if hour > 9 else '0' + str(hour)
        minute = str(minute) if minute > 9 else '0' + str(minute)
        if minute == 0:
            output = hour + ' Uhr.'
        elif minute == 5:
            output = 'fünf nach ' + hour
        elif minute == 10:
            output = 'zehn nach ' + hour
        elif minute == 15:
            output = 'viertel nach ' + hour
        elif minute == 20:
            output = 'zwanzig nach ' + hour
        elif minute == 25:
            output = 'fünf vor halb ' + hour
        elif minute == 30:
            output = 'halb ' + next_hour
        elif minute == 35:
            output = 'fünf nach halb ' + next_hour
        elif minute == 40:
            output = 'zwanzig vor ' + next_hour
        elif minute == 45:
            output = 'viertel vor ' + next_hour
        elif minute == 50:
            output = 'zehn vor ' + next_hour
        elif minute == 55:
            output = 'fünf vor ' + next_hour
        else:
            output = hour + ':' + minute + ' Uhr'
        return output

    @staticmethod
    def get_word_index(text, word):
        text = text.split(' ')
        for i in range(len(text)):
            if text[i] == word:
                return i
        return -1


    @staticmethod
    def is_desired(text):
        # returns True, if user want this option
        approvals = ['ja', 'gerne']
        if any(approvals) in text:
            return True
        elif 'bitte' in text and not 'nicht' in text:
            return True
        elif 'danke' in text and not 'nein' in text:
            return True
        return False

    class Statics:
        def __init__(self):
            pass

        # Colors
        color_ger_to_eng = {
            "schwarz": "black",
            "blau": "blue",
            "rot": "red",
            "gelb": "yellow",
            "grün": "green"
        }

        color_eng_to_ger = {
            "black": "schwarz",
            "blue": "blau",
            "red": "rot",
            "yellow": "gelb",
            "green": "grün"
        }

        # Weekdays
        weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        weekdays_engl = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        weekdays_ger_to_eng = {
            'montag': 'monday',
            'dienstag': 'tuesday',
            'mittwoch': 'wednesday',
            'donnerstag': 'thursday',
            'freitag': 'friday',
            'samstag': 'saturday',
            'sonntag': 'sunday'
        }

        weekdays_eng_to_ger = {
            'monday': 'montag',
            'tuesday': 'dienstag',
            'wednesday': 'mittwoch',
            'thursday': 'donnerstag',
            'friday': 'freitag',
            'saturday': 'samstag',
            'sunday': 'sonntag'
        }

        numb_to_day = {
            "1": "monday",
            "2": "tuesday",
            "3": "wednesday",
            "4": "thursday",
            "5": "friday",
            "6": "saturday",
            "7": "sunday"}

        numb_to_day_numb = {'01': 'ersten', '02': 'zweiten', '03': 'dritten', '04': 'vierten', '05': 'fünften',
                            '06': 'sechsten', '07': 'siebten', '08': 'achten', '09': 'neunten', '10': 'zehnten',
                            '11': 'elften', '12': 'zwölften', '13': 'dreizehnten', '14': 'vierzehnten',
                            '15': 'fünfzehnten',
                            '16': 'sechzehnten', '17': 'siebzehnten', '18': 'achtzehnten', '19': 'neunzehnten',
                            '20': 'zwanzigsten',
                            '21': 'einundzwanzigsten', '22': 'zweiundzwanzigsten', '23': 'dreiundzwanzigsten',
                            '24': 'vierundzwanzigsten',
                            '25': 'fünfundzwanzigsten', '26': 'sechsundzwanzigsten', '27': 'siebenundzwanzigsten',
                            '28': 'achtundzwanzigsten',
                            '29': 'neunundzwanzigsten', '30': 'dreißigsten', '31': 'einunddreißigsten',
                            '32': 'zweiunddreißigsten'}

        numb_to_hour = {'01': 'ein', '02': 'zwei', '03': 'drei', '04': 'vier', '05': 'fünf', '06': 'sechs',
                        '07': 'sieben', '08': 'acht', '09': 'neun', '10': 'zehn', '11': 'elf', '12': 'zwölf',
                        '13': 'dreizehn', '14': 'vierzehn', '15': 'fünfzehn', '16': 'sechzehn', '17': 'siebzehn',
                        '18': 'achtzehn', '19': 'neunzehn', '20': 'zwanzig', '21': 'einundzwanzig',
                        '22': 'zweiundzwanzig',
                        '23': 'dreiundzwanzig', '24': 'vierundzwanzig'}

        numb_to_month = {'01': 'Januar', '02': 'Februar', '03': 'März', '04': 'April', '05': 'Mai', '06': 'Juni',
                         '07': 'Juli', '08': 'August', '09': 'September', '10': 'Oktober', '11': 'November',
                         '12': 'Dezember'}
