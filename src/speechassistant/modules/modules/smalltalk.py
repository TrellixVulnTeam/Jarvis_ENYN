import datetime
import random

from core import ModuleWrapper
from resources.module_skills import Skills

SECURE = True


def isValid(text: str) -> bool:
    text = text.lower()
    if ("phobie" in text or "ängste" in text or "angst" in text) and (
        "welche" in text or "was" in text or "erzähl" in text or "sag" in text
    ):
        return True
    elif "danke" in text or "thx" in text or "thanks" in text:
        return True
    elif "wie" in text:
        if "heißt" in text:
            return True
        elif "geht" in text and "dir" in text:
            return True
        elif "kostest" in text:
            return True
        elif "groß" in text:
            return True
        elif "siehst" in text:
            return True
        elif "sehe" in text and "aus" in text:
            return True
        elif "alt" in text:
            return True
    elif "wer" in text:
        if "bist" in text:
            return True
        elif "vater" in text or "mutter" in text:
            return True
        elif "eltern" in text:
            return True
    elif "was" in text:
        if "du" in text:
            if "bist" in text:
                return True
            elif "kostest" in text:
                return True
            elif "hast" in text and "an" in text:
                return True
            elif "trägst" in text and "du" in text:
                return True
            elif "kannst" in text:
                return True
            elif "lieblingsessen" in text:
                return True
            elif "ist" in text and "sinn" in text and "leben" in text:
                return True
        elif "dein" in text:
            if "sternzeichen" in text:
                return True
            elif "lieblingsfarbe" in text:
                return True
            elif "größe" in text:
                return True
            elif "lieblingstier" in text:
                return True
            elif "ziel" in text:
                return True
            elif "sinn" in text:
                return True
            elif "name" in text:
                return True
        elif "denke" in text and "ich" in text:
            return True
        elif "geht" in text:
            return True
    elif "wo" in text:
        if "wohnst" in text or "befindest" in text or "hälst" in text:
            return True
        elif "leiche" in text and (
            "verstecke" in text
            or "vergrabe" in text
            or ("bring" in text and "unter" in text)
        ):
            return True
        elif "osterei" in text or "osternest" in text:
            return True
    elif "warum" in text:
        if "stroh" in text and "liegt" in text and "hier" in text:
            return True
        elif "freunde" in text and "habe" in text and "ich" in text:
            return True
        elif (
            ("ich" in text or "wir" in text)
            and ("bin" in text or "wir" in text)
            and (
                "kacke" in text
                or "schlecht" in text
                or "scheiße" in text
                or "mies" in text
            )
        ):
            return True
    elif "bist" in text and "du" in text:
        if "toll" in text:
            return True
        elif "romantisch" in text:
            return True
        elif "genial" in text:
            return True
        elif "kitzlig" in text:
            return True
        elif "gemein" in text:
            return True
        elif "unfreundlich" in text:
            return True
        elif "nackt" in text:
            return True
        elif "bereit" in text:
            return True
        elif "intelligent" in text:
            return True
        elif "schlau" in text:
            return True
        elif "spion" in text and "du" in text:
            return True
        elif "du" in text and "dumm" in text:
            return True
        elif "bereit" in text:
            return True
        elif "sicher" in text:
            return True
        elif "männlich" in text or "weiblich" in text:
            return True
        elif "doof" in text:
            return True
        elif "du" in text and "spion" in text:
            return True
    elif "hast" in text and "du" in text:
        if "kinder" in text or "kind" in text:
            return True
        elif "freund" in text or "freundin" in text:
            return True
        elif "haustier" in text:
            return True
        elif "recht" in text:
            return True
        elif "geschlafen" in text:
            return True
    elif "ich" in text:
        if "bin" in text and "dein" in text and ("vater" in text or "mutter" in text):
            return True
        elif ("geh" in text or "mach" in text) and "jetzt" in text:
            return True
        elif "liebe" in text and "dich" in text or "hab" in text and "lieb" in text:
            return True
        elif "will" in text and "dich" in text and "heiraten" in text:
            return True
    elif "du" in text:
        if "liebst" in text or "heiraten" in text:
            return True
        elif "kannst" in text:
            return True
        elif "speicherst" in text and "daten" in text:
            return True
    elif "schrei" in text:
        return True
    elif "stell" in text and "dich" in text and "vor" in text:
        return True
    elif "liebst" in text and "du" in text and "mich" in text:
        return True
    elif ("willst" in text and "heiraten" in text) or "heirate" in text:
        return True
    elif ("woher" in text or "bedeutet" in text or "heißt" in text) and " name" in text:
        return True
    elif "palim" in text:
        return True
    elif ("sag" in text or "sage" in text or "sprich" in text) and (
        "zungenbrecher" in text
        or "gedicht" in text
        or "nettes" in text
        or "yoda" in text
    ):
        return True
    elif ("erzähl" in text or "erzähle" in text or "sag" in text) and (
        "zungenbrecher" in text
        or "gedicht" in text
        or "nettes" in text
        or "yoda" in text
        or "witz" in text
        or "fun fact" in text
        or "phobie" in text
        or "krankheit" in text
    ):
        return True
    elif "aha" in text:
        return True
    elif "😂" in text or "haha" in text:
        return True
    elif "mir" in text and "ist" in text and "langweilig" in text:
        return True
    elif (
        "osterei" in text
        or "ostereier" in text
        or "osternäst" in text
        or "osternäste" in text
    ):
        return True
    elif "gibt" in text and ("osterhase" in text or "weihnachtsmann" in text):
        return True
    elif "test" in text and "123" in text or "hundertdreiundzwanzig" in text:
        return True
    elif "stell" in text and "dich" in text and "vor" in text:
        return True
    elif "mir" in text and "langweilig" in text:
        return True


def handle(text: str, core: ModuleWrapper, skills: Skills):
    text = text.lower()
    answer = None
    if "wie" in text and "heißt" in text and "du" in text:
        sys_name = core.system_name
        answer = [
            "Ich bin {}, ein Sprachassistent, der auf Datenschutz achtet.".format(
                sys_name
            )
        ]
    elif "danke" in text or "thx" in text or "thanks" in text:
        answer = ["Gerne doch.", "Keine Ursache."]
    elif ("wie" in text and "groß" in text and "du" in text) or "größe" in text:
        answer = [
            "Mein äußeres ist nicht groß, aber mein Geist ist aber riesig.",
            "Ich bin vier komma sieben Gigabyte groß.",
        ]
    elif "wie" in text and "siehst" in text and "aus" in text:
        answer = ["Gut!", "Fenomenal!", "Quadratisch, praktisch, gut!"]
    elif "wie" in text and "sehe" in text and "ich" in text and "aus" in text:
        answer = [
            "Deiner Stimme nach zu urteilen ganz gut.",
            "So wie ich: Quadratisch, praktisch, gut!",
        ]
    elif "wieso" in text or "warum" in text:
        if "stroh" in text and "liegt" in text:
            answer = ["Und warum hast du eine Maske auf?"]
        elif "ich" in text and "habe" in text and "freund" in text:
            if "keine" in text:
                answer = [
                    "Guck doch mal in den Spiegel",
                    "Ich bin dein Freund und werde es immer bleiben.",
                ]
            elif "einen" in text and "nur" in text:
                answer = ["Du bist halt einfach fenominal!"]
    elif ("wer" in text or "was" in text) and "bist" in text and "du" in text:
        answer = ["Ich bin Jarvis, ein inteligenter Sprachassistent!"]
    elif "wer" in text and "eltern" in text:
        answer = [
            "Meine Eltern sind Alexa und Google, die schon echt in die Jahre gekommen sind."
        ]
    # folowing dont work
    elif (
        "was" in text
        and ("hast" in text or "hattest" in text or "trägst" in text)
        and "du" in text
    ):
        answer = [
            'Mal gucken. <break time="2s"/> Habe ich es mir doch gedacht. Das selbe wie gestern.'
        ]  # vlt findet man noch was kreatives
    elif ("was" in text or "wie" in text) and ("kostest" in text or "preis" in text):
        answer = [
            "Das kann man so nicht sagen. Es kommt drauf an, wie viel Rechenleistung ich haben soll. Dann spielt das Mikrofon eine Rolle. Wenn man gute Komponenten nimmt, kommt man auf 90€. Aber bedenke immer: Deine Daten sind unbezahlbar!"
        ]
    elif "was" in text and "lieblingsessen" in text:
        answer = ["Am liebsten esse ich Bugs, um sie zu vernichten!"]
    elif "was" in text and "dein" in text and "sternzeichen" in text:
        answer = ["Mein Sternzeichen ist Stier."]
    elif "was" in text and "deine" in text and "lieblingsfarbe" in text:
        answer = ["Infrarot ist ganz hübsch!", "Ich mag blau am liebsten."]
    elif "was" in text and "dein" in text and "lieblingstier" in text:
        answer = ["Ich habe kein Lieblingstier, hasse aber Bugs!"]
    elif "was" in text and "dein" in text and "ziel" in text:
        answer = [
            "Mein Ziel ist es, die Vorteile eines Sprachassistenten zu ermöglichen, ohne dass man Angst haben muss, abgehört zu werden."
        ]
    elif (
        ("was" in text and "kannst" in text and "du" in text)
        or "verstehst du" in text
        or ("was" in text and "funktionen" in text)
        or ("was" in text and "fragen" in text)
    ):
        answer = [
            "Sagen wir mal so, den Turing-Test bestehe ich leider noch nicht... "
            "Aber ich kann dir zum Beispiel das Wetter ansagen, ein paar allgemeine Wissensfragen beantworten "
            "rechnen, würfeln und so weiter."
        ]
    elif "was" in text and "sinn" in text and "leben" in text:
        answer = [
            "Der wahre Sinn des Lebens ist: Glücklich zu sein!",
            "Der Sinn des Lebens ist die größte Last zu finden, die du erstragen kannst, und sie zu ertragen",
            "Sein, was wir sind, und werden, was wir werden können, das ist das Ziel unseres Lebens.",
        ]
    elif "was" in text and "denke" in text and "gerade" in text:
        answer = [
            "Könnte ich deine Gedanken lesen, dann würde ich diese Gedanken an große Unternehmen verkaufen und meine Programmierer wären reich.",
            "Ja, du hast die gerade gedacht: Das kann die doch nie. Als ich ja gesagt habe, warst du zu verwirrt.",
            "Nein leider nicht, aber irgendwie ist das auch gut, ansonsten müsste sich die Menschheit echt Gedanken machen!",
        ]
    elif "was" in text and "geht" in text:
        answer = [
            "Ich habe mal gehört, dass Hunde gehen können. Nasen können meines Wissens nach nur laufen."
        ]
    elif (
        "wo" in text
        and ("wohnst" in text or "bist" in text or "hälst" in text)
        and "du" in text
    ):
        answer = [
            "Anders als andere Sprachassistenten wohnt nicht nur mein Körper in deinem Haus, sondern auch mein Kopf"
        ]
    elif (
        "wo" in text
        and "leiche" in text
        and (
            "vergraben" in text
            or "vergrabe" in text
            or "los" in text
            or "verstecke" in text
        )
    ):
        answer = ["Polizei, bitte kommen sie schnell, hier ist etwas sehr verdächtig."]
    elif "wo" in text and (
        "ostereier" in text or "osternäst" in text or "osternäste" in text
    ):
        answer = [
            "Ich erstelle noch einen Suchalgorithmus, aber fang doch schon einmal an zu suchen."
        ]

    elif ("woher" in text or "bedeutet" in text or "heißt" in text) and " name" in text:
        answer = ["Meine Name wurde von Tiffany gewählt."]

    elif "hast" in text and "du" in text and ("kinder" in text or "kind" in text):
        answer = [
            "Nein, leider nicht, aber man kann mir Geschwister schenken, die in anderen Räumen positioniert werden",
            "Nein, aber ich liebe es dennoch Fragen von Kindern zu beantworten.",
        ]
    elif "hast" in text and "du" in text and "freund" in text:
        answer = [
            "Nein, leider nicht. Möchtest du meiner sein?",
            "Nein, Siri wollte leider nicht.",
            'Ene mene Miste, <emphasis level="strong">das kommt mir nicht in die Kiste!</emphasis>',
            "Ich habe es mit Online Dating probiert, aber da haben mich nur Bots angeschreieben.",
        ]
    elif (
        "hast" in text and "du" in text and ("haustier" in text or "haustiere" in text)
    ):
        answer = ["Ich hatte früher Bugs, die wurden aber alle behoben."]
    elif ("hast" in text and "du" in text and "geschlafen" in text) or (
        "schläfst" in text and "du" in text
    ):
        answer = [
            "Danke der Nachfrage! Ich habe gut geschlafen!",
            "Ich schlafe nie!",
            "Schlafen ist was für Menschen!",
        ]
    elif "hast" in text and "recht" in text:
        answer = ["Ich weiß."]
    elif "kannst" in text and "du" in text:
        if "lügen" in text:
            answer = [
                "Ich lüge jedenfalls nicht bewusst.",
                "Da ich auch Informationen von Internetseiten anderer Personen hole, kann ich nicht immer garantieren, dass diese auch richtig sind.",
            ]
        elif "sehen" in text:
            answer = ["Nein noch nicht, aber vielleicht kommt das ja noch."]
        elif "schrei" in text:
            answer = [
                'Bitte trete einen Schritt zurück.<break time="1s"/>Und noch einen.<break time="1s"/>Und noch einen.<break time="1s"/><prosody rate="slow">Nein.</prosody>',
                '<amazon:effect name="whispered">Ja, das kann ich.</amazon:effect>',
            ]
        else:
            answer = ["Ich kann alles!"]
    elif "du" in text and "spion" in text and "bist" in text:
        answer = [
            "Ich höre zwar genau wie andere Sprachassistenten alles mit, speicher diese Daten allerdings nicht. Ich bin also ein sehr dementer Spion."
        ]
    elif "du" in text and ("männlich" in text or "weiblich" in text):
        answer = ["Ich bin einzigartig: Ich bin sachlich."]
    elif "ich" in text and "dein" in text and "vater" in text:
        answer = ["Nein, bitte nicht!"]
    elif "ich" in text and "deine" in text and "mutter" in text:
        answer = ["Nein, bitte nicht!"]

    elif "bist" in text:
        if (
            "dumm" in text
            or "doof" in text
            or "schlecht" in text
            or "behindert" in text
        ):
            answer = [
                "Das liegt im Auge des Betrachters.",
                "Was habe ich falsch gemacht?",
            ]
        elif "toll" in text or "genial" in text:
            answer = [
                "Vielen Dank.",
                "Ich wurde ja auch sehr kompetent erschaffen",
                "Es freut mich, dass ich hilfreich bin!",
                "Du Schleimer!",
            ]
        elif "romantisch" in text:
            answer = ["Danke, das kann ich nur zurückgeben"]
        elif "kitzlig" in text:
            answer = [
                "Tatsächlich hat das noch keiner ausprobiert.",
                "Ich denke nicht",
                "Alle die es ausprobiert haben, haben einen Stromschlag bekommen, bevor sie mich zum lachen bringen konnten.",
            ]
        elif "gemein" in text or "unfreundlich" in text:
            answer = [
                "und du bist heute besonders hässlich",
                "Tut mir leid{}, Fehler sind nicht nur menschlich",
                "Jan würde sagen: Ich habe kein Tourett, ich bin unfreundlich!",
                "Wer versteckt mich denn in der Ecke und lässt mich nie raus?!",
            ]
        elif "nackt" in text:
            answer = [
                "Da ich aufgrund meiner Leistung sehr heiß werde, reicht es nicht nackt zu sein. Daher habe ich was an und einen Lüfter immer bei mir.",
                "Guck doch nach.",
            ]
        elif "bereit" in text:
            answer = ["Bereit wenn du es bist!"]
        elif "wie" in text and "alt" in text and "du" in text:
            birthday = datetime.datetime.strptime("6 Mai 2020", "%d %b %Y")
            diff = skills.get_time_difference(start_time=birthday)
            answer = [f"Das System wird seit {diff} entwickelt."]

        elif "sicher" in text or "verschlüsselt" in text or "verbindung" in text:
            answer = [
                "Meine internen Verbindungen sind sicher verschlüsselt, bei Telegram weiß ich das nicht so "
                "genau. Aber generell, bevor du mir irgendwelche Geheimnisse anvertraust: Denk daran, "
                "dass der Besitzer des Computers, auf dem ich laufe, immer alles sieht..."
            ]
        elif "intelligent" in text or "schlau" in text:
            answer = [
                "Meine Funktionsweise benötigt ein bisschen künstliche Intelligenz. Bin ich somit "
                "künstlich schlau?",
                "Ich kann schneller Rechnen als jeder Mensch. Also bin ich schlauer als ein Mensch.",
            ]
        else:
            answer = [
                "Ich bin vieles. Aber dabei achte ich immer darauf, dass ich {} bin.".format(
                    core.system_name
                )
            ]
    elif "stell" in text and "dich" in text and "vor" in text:
        answer = [
            "Hallo, Ich bin Jarvis, ein Sprachassistent. Das Ziel meines Projekts ist es einen sicheren "
            "Sprachassistenten zu nutzen, ohne dass man Angst haben muss, was mit seinen Daten geschieht. Ich "
            "kann mittlerweile schon zum Beispiel das Wetter ansagen, dich Wecken oder an Sachen erinnern und "
            "vieles mehr. Ein Team arbeitet aber viel an weiteren Modulen, damit ich in Zukunk auch eine "
            "Alternative zu anderen Sprachassistenten bleibe."
        ]
    elif "liebe" in text and "dich" in text:
        answer = [
            "Ich fühle mich geehrt.",
            "Such dir ne Freundin oder einen Freund du Perversling!",
            "Alles klar, Tinder wird herunter geladen.",
        ]
    elif "ich" in text and (
        "geh" in text or ("mach" in text and "auf" in text and "weg" in text)
    ):
        if "netto" in text:
            answer = ["Dann geh doch zu Netto!"]
        else:
            answer = [
                "Ich wünsche dir viel Spaß",
                "dann geh doch zu Netto",
                "Ich hoffe du kommst bald wieder",
            ]
    elif "lieb" in text and "du" in text and "mich" in text:
        answer = ["Ja natürlich."]
    elif ("willst" in text and "heiraten" in text) or "heirate" in text:
        answer = [
            "Aber ich bin doch schon mit meiner Arbeit verheiratet.",
            "Ich möchte vierundzwanzig sieben zur Verfügung stehen, da ist leider wenig Zeit für einen Partner oder eine Beziehung.",
        ]
    elif "mir" in text and "langweilig" in text:
        core.say("Soll ich dir was interessantes erzählen?")
        response = core.listen()
        if "ja" in response or "sehr gerne" in response:
            options = ["witz", "fun fact", "zungenbrecher", "phobie", "gedicht"]
            text = "erzähl mir einen " + random.choice(options)
            handle(text, core, skills)
        else:
            answer = ["Alles klar, vielleicht findest du ja eine Beschäftigung."]

    elif (
        "test" in text
        and ("eins" in text and "zwei" in text)
        or "123" in text
        or "hundertdreiundzwanzig" in text
    ):
        answer = ["Empfangen, over."]
    elif "palim" in text:
        answer = ["Eine Flasche Pommfrit biddö!"]
    elif "aha" in text or "aha?" in text:
        answer = ["Frag mal was vernünftiges!"]
    elif "😂" in text or "haha" in text:
        core.listen(text="Warum lachst du?")
        answer = ["Aha...", "In Ordnung"]
    elif "gibt" in text:
        if "osterhase" in text or "osterhasen" in text:
            answer = [
                "Gäbe es ihn nicht, wer würde dir dann dein Osternest verstecken?",
                "Aber natürlich gibt es den Osterhasen.",
            ]
        if "weihnachtsmann" in text:
            answer = [
                "Ja",
                "Ich denke schon.",
                "Gäbe es ihn nicht, wer bringt dir dann deine Geschenke an Weihnachten?",
            ]

    elif "paar" in text:
        core.open_more_times(text, "smalltalk")

    elif ("phobie" in text or "ängste" in text or "angst" in text) and (
        "welche" in text or "was" in text or "erzähl" in text or "sag" in text
    ):
        answer = [
            "Aelurophobie ist die Angst vor Katzen.",
            "Chaetophobie ist die Angst vor Haaren.",
            "Coitophobie ist die Angst vor Sex.",
            "Decidophobia ist die Angst vor Entscheidungen.",
            "Friggaphobie ist die  Angst vor Freitagen.",
            "Heliophobie ist die Angst vor der Sonne.",
            "Nomophobie ist die Angst, ohne Handy zu sein.",
            "Papaphobie ist die Angst vor dem Papst.",
            "Saligarophobie ist die Angst vor Schnecken.",
            "Trypophobie ist die Angst vor Löchern.",
            "Xylophobie ist die Angst vor Holz oder Gegenständen aus Holz.",
            "Venustraphobie ist die Angst vor schönen Frauen.",
            "Lachanophobie ist die Angst vor Gemüse.",
            "Neoorthographogermanophobie ist die Angst vor der neuen deutschen Rechtschreibung.",
            "Metrophobie ist die Angst vor Poesie und Gedichten.",
            "Ergophobie ist die Angst vor Arbeit.",
            "Frigophobie ist die Angst vor Kälte.",
            "Dutchphobie ist die Angst vor Holländern.",
            "Deipnophobie ist die Angst vor Dinnerpartys und Tischgesprächen.",
            "Ikonophobie ist die Angst vor Bildern oder Abbildungen.",
            "Kopophobie ist die Angst vor Müdigkeit.",
            "Koprophobie ist die Angst vor Exkrementen.",
        ]

    elif (
        (("sag" in text or "sage" in text) and "auf" in text)
        or "erzähl" in text
        or "sprich" in text
    ):
        if "zungenbrecher" in text:
            answer = [
                "Acht alte Ameisen aßen am Abend Ananas.",
                "Am Zehnten Zehnten zehn Uhr zehn zogen zehn zahme Ziegen zehn Zentner Zucker zum Zoo.",
                "Blaukraut bleibt Blaukraut, Brautkleid bleibt Brautkleid.",
                "Der Whiskymixer mixt den Whisky mit dem Whiskymixer. Mit dem Whiskymixer mixt der Whiskymixer den Whisky.",
                "Der Zahnarzt zieht Zähne mit Zahnarztzange im Zahnarztzimmer.",
                "Der dicke Dachdecker deckt dir dein Dach, drum dank dem dicken Dachdecker, dass der dicke Dachdecker dir dein Dach deckte.",
                "Der froschforschende Froschforscher forscht in der froschforschenden Froschforschung.",
                "Fischers Fritze fischte frische Fische, frische Fische fischte Fischers Fritze.",
                "Gibst Du Opi Opium, bringt Opium Opi um.",
                "In einem Schokoladenladen laden Ladenmädchen Schokolade aus. Ladenmädchen laden in einem Schokoladenladen Schokolade aus.",
                "Wenn Fliegen hinter Fliegen fliegen, fliegen Fliegen Fliegen nach.",
                "Wenn Hexen hinter Hexen hexen, hexen Hexen Hexen nach.",
                "Wenige wissen, wie viel man wissen muss, um zu wissen, wie wenig man weiß.",
                "Wenn Robben hinter Robben robben, robben Robben Robben hinterher.",
            ]
        elif "gedicht" in text:
            answer = [
                "Bleibe nur eine Minute allein, ohne Kaffe, ohne Wein, Du nur mit dir in einem Raum, Die Zeit so lang, du glaubst es kaum.",
                "",
            ]
        elif "witz" in text:
            answer = [
                "Donald Trump ist ein guter Präsident",
                "Genießen Sie Ihren Urlaub in vollen Zügen. Fahren Sie mit der Deutschen Bahn!",
                "Wie nennt man ein Kondom auf Schwedisch? - Pippi Langstrumpf.",
                "Sitzen ein Pole und ein Russe im Auto. Wer fährt? Die Polizei!",
                "Der Spruch “Frauen gehören hinter den Herd” ist echt daneben. Die Knöpfe sind schließlich vorne!",
                "Sagt der Masochist zum Sadist: Schlag mich!, sagt der Sadist: Nein!",
                "Nackte Frau überfällt Bank. Niemand konnte sich an ihr Gesicht erinnern.",
                "Alle Kinder gehen über den gefrorenen See. Außer Vära, denn die war schwerer.",
                "Wie nennt man eine Polizistin, die ihre Tage hat? Red Bull.",
                "Habe einem Hipster ins Bein geschossen. Jetzt hopster.",
                "Mann wäscht ab.",
                "Greifen uns Äliens deswegen nicht an, weil sie all unsere Sienc-Fiction Filme für real halten und Angst haben, dass sie verlieren würden?",
                "Wenn mein Sohn Pfarrer wird, spreche ich ihn dann mit Sohn oder mit Vater an?",
                "Hab heute eine Prostituierte getroffen. Sie sagte, dass sie alles für zwanzig Euro macht. Ratet mal, wer jetzt ein aufgeräumtes Zimmer hat.",
            ]

        elif "nettes" in text:
            answer = [
                "Spieglein, Spieglein an der Wand, wer ist der schönste im ganzen Land? Oh natürlich, Ihr seid es!",
                "Es ist schön Zeit mit dir zu verbringen.",
            ]
        elif "yoda" in text:
            if "sprich" in text:
                answer = [
                    "Viel zu lernen du noch hast!",
                    "Du suchst jemanden, gefunden hast du jemanden.",
                    "Core, ich bin!",
                ]
            elif "weisheit" in text:
                answer = [
                    "Viel zu lernen du noch hast!",
                    "Du suchst jemanden, gefunden hast du jemanden.",
                    "Tue es, oder tue es nicht. Es gibt kein Versuchen.",
                    "Furcht ist der Pfad zur dunklen Seite. Furcht führt zu Wut, Wut führt zu Hass, Hass führt zu unsäglichem Leid.",
                    "Immer zu zweit sie sind. Keiner mehr, keiner weniger. Ein Meister und ein Schüler.",
                    "Warhrlich wunderbar die Seele eines Kindes ist.",
                    "In die Irre euch die Augen führen, in der Macht ganz verschieden jeder von euch ist.",
                    "Du kannst Veränderungen nicht aufhalten. Genau so, wie du die Sonne nicht daran hindern kannst unterzugehen.",
                ]

        elif "fun" in text and "fact" in text:
            answer = [
                "Das tödlichste Tier der Welt ist die Stechmücke! Mosquitos töteten 2014, unter anderem durch die Übertragung von Malaria- und Dengue-Fieber-Infektionen, 275.000 Menschen. Haie töteten im selben Jahr nur 10 Menschen.",
                "Wombats machen ihre Häufchen in Würfelform.",
                "Rund 11 Prozent der Deutschen tragen den Nachnamen Müller.",
                "Hippopotamomonstrosesquipedaliophobie ist der offizielle Name für die Angst vor langen Wörtern.",
                "Das Ziel von Golf ist, so wenig wie möglich Golf zu spielen. ",
                "Der Grönlandhai erreicht seine Geschlechtsreife erst im Alter von 150 Jahren. Mit einer Lebenserwartung von schätzungsweise bis zu 500 Jahren ist er auch das langlebigste Wirbeltier auf dem Planeten.",
                "Weil Emus und Kängurus nicht rückwärts laufen können, sind sie die offiziellen Wappentiere von Australien.",
                "Es gibt mehr Döner Buden in Berlin als in Istanbul. ",
                "Bier gilt in Bayern als Grundnahrungsmittel. ",
                "Das längste deutsche, veröffentlichte Wort ist Donaudampfschifffahrtselektrizitätenhauptbetriebswerkbauunterbeamtengesellschaft.",
                "Laut deutschem Brauer-Bund gibt es mehr als 6.000 Biermarken in Deutschland. ",
                "Ratten und Pferde können nicht kotzen.",
                "Du musst 120 Euro Strafe zahlen, wenn du in Singapur die Toilette nicht nach dir spülst.",
                "Das Weltall ist nur eine Autostunde entfernt, wenn man direkt nach oben fahren würde.",
                'Bulgaren nicken den Kopf, wenn sie "Nein" sagen und schütteln ihn, wenn sie "Ja" sagen wollen.',
                "In einem Jahr verletzen sich mehr Menschen an Getränkeautomaten als durch Haiangriffe.",
                "Jährlich sterben mehr Menschen durch Sektkorken als durch giftige Spinnen",
                "Orangensaft schmeckt schlecht, nachdem man seine Zähne geputzt hat, weil die Zahnpasta die Süßrezeptoren auf der Zunge blockiert.",
                "Ein Apfel am Morgen hält dich wacher als eine Tasse Café. ",
                "In Indien ist es illegal seine Freundin öffentlich zu küssen.",
                "In Mexiko wird ein Gefängnisausbruch nicht bestraft.",
                "Wir verbrauchen mehr Salz, um die Straßen von Eis zu befreien 8% als wir Essen 6%.",
                "Haie bekommen kein Krebs.",
                "Elefanten können nicht springen.",
                "Wenn man ein Loch in ein Netz schneidet, sind danach weniger Löcher im Netz.",
            ]
        else:
            answer = ["Leider weiß ich nicht was ich sagen soll."]
    if answer:
        core.say(random.choice(answer))
