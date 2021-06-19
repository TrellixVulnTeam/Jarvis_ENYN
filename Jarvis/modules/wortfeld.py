import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud

def isValid(text):
    if ('erstell' in text or 'generier' in text) and ('wortfeld' in text or 'wordmap' in text or 'wortwolke' in text):
        return True
    return False


def handle(text, core, skills):
    #toDo: img not found
    char_mask = np.array(Image.open('Jarvis/modules/resources/temp/word_field.png'))

    words = core.listen('Bitte nenne nun die Wörter, die in einem Bild zusammengefasst werden sollen. Jedes Wort muss mit einem "," oder einem "und" voneinander abgetrennt werden.')
    words = words.replace(' und ', ', ')

    bg_color = "black"
    for color in skills.Statics.color_ger_to_eng.keys():
        if color in text:
            bg_color = skills.Statics.color_ger_to_eng.get(color)
    word_cloud = WordCloud(background_color=bg_color, mask=char_mask).generate(words)

    plt.figure(figsize=(8,8))
    plt.imshow(word_cloud)

    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    class Core:
        def listen(self, text=""):
            return input(text)
        def say(self, text):
            print(text)

    handle("", Core(), None)