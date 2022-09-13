from src.modules import ModuleWrapper
from src.modules.batches import batchMatch


def is_valid(text: str) -> bool:
    text = text.lower()
    batch = ["[wandle|wandel|gib|was] [|gibt|ist] [|in|auf] binär"]
    return batchMatch(batch, text)


def handle(text: str, wrapper: ModuleWrapper) -> None:
    decNumber = getNumber(text)
    if decNumber != "UNDO":
        wrapper.say(f"Die Zahl {decNumber} ist {__calculate_binary(int(decNumber))} in dem Binären.")
    else:
        wrapper.say("Ich konnte die Zahl leider nicht herausfiltern.")


def __calculate_binary(number: int) -> str:
    output = ""
    while number > 0:
        output = f"{number % 2}{output}"
        number = number // 2
    return str(output)


def getNumber(text: str):
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
