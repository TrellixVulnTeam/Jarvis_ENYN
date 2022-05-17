def isValid(text):
    text = text.lower()
    if "übersetz" in text:
        return True


def handle(text, core, skills):
    # toDo: was heißt auf
    traslation_text = skills.get_text_between(
        "übersetz", text, end_word="ins", output="String"
    )
    targetLang = skills.get_text_between("ins", output="String")
    core.translate(traslation_text, targetLang=targetLang)


def get_text_beetween(start_word, text, end_word="", output="array"):
    ausgabe = []
    index = -1
    text = text.split(" ")
    for i in range(len(text)):
        if text[i] is start_word:
            index = i + 1
    if index is not -1:
        if end_word is "":
            while index <= len(text):
                ausgabe.append(text[index])
                index += 1
        else:
            founded = False
            while index <= len(text) and not founded:
                if text[index] is end_word:
                    founded = True
                else:
                    ausgabe.append(text[index])
                    index += 1
    if output is "array":
        return ausgabe
    elif output is "String":
        ausgabe_neu = ""
        for item in ausgabe:
            ausgabe += item + " "
        return ausgabe
