from src.modules import ModuleWrapper
from src.modules.batches import batchMatch


# toDO: rework

def isValid(text: str) -> bool:
    text = text.lower()
    batch = ["[wandle|wandel|gib|was] [|gibt|ist] [|in|auf] binär"]
    return batchMatch(batch, text)


def handle(text: str, wrapper: ModuleWrapper) -> None:
    decNumber = getNumber(text)
    if decNumber != "UNDO":
        wrapper.say(
            "Die Zahl "
            + decNumber
            + " ist "
            + binary(int(decNumber))
            + " in dem Binären."
        )
    else:
        wrapper.say("Ich konnte die Zahl leider nicht herausfiltern.")


def binary(n):
    output = ""
    while n > 0:
        output = "{}{}".format(n % 2, output)
        n = n // 2
    return str(output)


def getNumber(text):
    answer = "UNDO"
    hotWord = ["wandle", "wandel", "gib", "ist"]
    sentence = text.split(" ")
    index = -1
    for item in sentence:
        i = 0
        while i <= len(hotWord):
            if sentence[item] == hotWord[i]:
                index = i + 1
    if index != -1:
        answer = sentence[index]
    return answer
