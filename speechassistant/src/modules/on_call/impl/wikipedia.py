#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from src.modules import ModuleWrapper, skills
from src.modules.on_call.utils.batches import batchMatch
import wikipedia

PRIORITY = -1
SECURE = True


# toDo: refactor

# wikipedia.set_lang("de")


def is_valid(text: str) -> bool:
    text = text.lower()
    batch = [
        "was weißt du über",
        "[was|wer] [ist|sind|war|waren]",
    ]
    if skills.match_any(text, " mal ", " plus ", " minus", " geteilt "):
        return False
    elif batchMatch(batch, text) or "was versteh" in text or "definier" in text:
        return True
    else:
        return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    text = text.lower().replace("ß", "ss")
    try:
        if "über" in text:
            article = text.split("über ")[1]
        elif (
                "was ist" in text
                or "wer ist" in text
                or "wer war" in text
                or "was war" in text
        ):
            article = (
                text.split("ist ")[1]
                if len(text.split("ist ")) >= 2
                else text.split(" war")[1]
            )
        elif (
                "was sind" in text
                or "wer sind" in text
                or "wer waren" in text
                or "was waren" in text
        ):
            article = (
                text.split("sind ")[1].rstrip("s")
                if len(text.split("ist ")) >= 2
                else text.split(" waren")[1].rstrip("s")
            )
        elif "was " in text and (" ist" in text or " sind" in text):
            article = (
                text.split("was ")[1]
                .split(" ist")[0]
                .split(" sind")[0]
                .split(" war")[0]
                .split(" waren")[0]
            )
        elif "wer " in text and (" ist" in text or " sind" in text):
            article = (
                text.split("wer ")[1]
                .split(" ist")[0]
                .split(" sind")[0]
                .split(" war")[0]
                .split(" waren")[0]
            )
        elif "unter" in text:
            article = text.split("unter ")[1]
        elif "definier" in text:
            article = " ".join(text.split("defi")[1].split(" ")[1:])
            article = masstrip(article, ["uns ", "mir ", "ihr ", "ihm "])
        else:
            article = "fehler"
        article = article.strip().strip("bitte")
        article = masstrip(
            article,
            ["ein ", "eine ", "einen ", "der ", "die ", "das ", " ist", " sind"],
        )
        try:
            wikitext = wikipedia.summary(article)
            wikitext = shorten(wikitext)
            wrapper.say("Ich habe folgendes herausgefunden: " + wikitext)
        except wikipedia.exceptions.DisambiguationError as e:
            succ = False
            for el in e.options:
                if succ is True:
                    break
                next = el.strip()
                try:
                    wikitext = wikipedia.summary(next)
                    wikitext = shorten(wikitext)
                    outstr = (
                            "Leider bin ich mir nicht ganz sicher, was du mit dem Begriff "
                            + article
                            + " meintest. "
                    )
                    outstr += (
                            "Am ehesten passte für mich der Begriff "
                            + next
                            + ", den ich deshalb für dich beschreibe. "
                    )
                    outstr += wikitext
                    succ = True
                except wikipedia.exceptions.DisambiguationError as ef:
                    print("EEERRR", ef)
                    outstr = "Leider kann ich dir im Moment nichts darüber erzählen. vielleicht versuchst du, deine Frage klarer zu formulieren?"
                except wikipedia.exceptions.PageError:
                    wrapper.say(
                        "Ich habe zwar Antworten gefunden, aber keine davon passt so richtig auf deine Frage. Entschuldige."
                    )
            wrapper.say(outstr)
        except wikipedia.exceptions.PageError:
            wrapper.say(
                "Leider weiß ich keine Antwort auf deine Frage. Vielleicht hilft dir eine Suche im Internet weiter?"
            )
    except IndexError:
        wrapper.say(
            "Leider hast du deine Frage so forumliert, dass ich sie nicht verstehen konnte. Das tut mir leid, versuch s doch einfach erneut!"
        )


## WIKIPEDIA-extract first sentence


def shorten(long):
    short = ""
    for block in long.split(")"):
        short += block.split("(")[0]
    cutsen = 1
    output = ""
    while cutsen <= 5:
        t_output = ". ".join(short.split(".")[0:cutsen]) + "."
        if len(t_output) <= 130 or t_output[-2] in "0123456789":
            cutsen += 1
        else:
            output = t_output
            cutsen = 10
        cutsen += 1
    output = (
        output.replace("  ", " ")
        .replace("..", ".")
        .replace(". .", ".")
        .replace(" ,", ",")
        .replace(" . ", ". ")
    )
    return output


def masstrip(input, blacklist):
    for word in blacklist:
        input = input.replace(word, "")
    return input.strip()
