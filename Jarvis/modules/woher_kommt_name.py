import random
from os import listdir
import string
import unicodedata
import torch
import torch.nn as nn
from torch.autograd import Variable
import matplotlib.pyplot as plt

letters = string.ascii_letters + ".,:'"

def toAscii(s):
    return ''.join(
        char for char in unicodedata.normalize('NFD', s)
        if unicodedata.category(char) != 'Mn'
        and char in letters
    )

def lines(datei):
    f = open(datei, encoding='utf-8').read().strip().split('\n')
    return [toAscii(l) for l in f]

def charToIndex(char):
    return letters.find(char)

def charToTensor(char):
    ret = torch.zeros(1, len(letters)) #ret.size = (1, len(letters))
    ret[0][charToIndex(char)] = 1
    return ret

def nameToTensor(name):
    ret = torch.zeros(len(name), 1, len(letters))
    for i, char in enumerate(name):
        ret[i][0][charToIndex(char)] = 1
    return ret

data = {}
languages = []
for f in listdir("./resources/namensherkunft/"):
    lang = f.split('.')[0]
    ls = lines("./resources/namensherkunft/" + f)
    languages.append(lang)
    data[lang] = ls

class AiNet(nn.Module):
    def __init__(self, input, hiddens, output):
        super(AiNet, self).__init__()
        self.hiddens = hiddens
        self.hid = nn.Linear(input + hiddens, hiddens)
        self.out = nn.Linear(input + hiddens, output)
        self.logsoftmax = nn.LogSoftmax(dim=1)

    def forward(self, x, hidden):
        x = torch.cat((x, hidden), 1)
        new_hidden = self.hid(x)
        output = self.logsoftmax(self.out(x))
        return output, new_hidden

    def init_hidden(self):
        return Variable(torch.zeros(1, self.hiddens))

model = AiNet(len(letters), 128, len(data))

def langFromOutput(out):
    _, i = out.data.topk(1)
    return languages[i[0][0]]

def getTrainData():
    lang = random.choice(languages)
    name = random.choice(data[lang])
    name_tensor = Variable(nameToTensor(name))
    lang_tensor = Variable(torch.LongTensor([languages.index(lang)]))
    return lang, name, lang_tensor, name_tensor

criterion = nn.NLLLoss()
def train(lang_tensor, name_tensor):
    hidden = model.init_hidden()
    model.zero_grad()
    for i in range(name_tensor.size()[0]):
        output, hidden = model(name_tensor[i], hidden)
    loss = criterion(output, lang_tensor)
    loss.backward()
    for i in model.parameters():
        i.data.add_(-0.01, i.grad.data)
    return output, loss

avg = []
sum = 0
for i in range(1, 100000):
    lang, name, lang_tensor, name_tensor = getTrainData()
    output, loss = train(lang_tensor, name_tensor)
    sum = sum + loss.data[0]

    if i%1000 == 0:
        avg.append(sum/1000)
        sum = 0
        print(i/1000, "% done.")

plt.figure()
plt.plot(avg)
plt.show()



