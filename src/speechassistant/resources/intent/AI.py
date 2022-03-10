from __future__ import annotations      # compatibility for < 3.10

import json
import logging
import os
import pickle
import random
from typing import Tuple
import numpy as np
import tensorflow.lite.python.lite

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import SGD, Adadelta

import matplotlib.pyplot as plt

nltk.download('omw-1.4', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)


class GenericAssistant:

    def __init__(self, intents: dict, path_extension: str, intent_methods: dict = {}, model_name: str = "assistant_model", json_encoding: str = 'utf-8') -> None:
        self.intents: dict = intents
        self.intent_methods: dict = intent_methods
        self.model_name: str = model_name
        self.json_encoding: str = json_encoding
        self.path_extension: str = path_extension

        if intents.endswith(".json"):
            self.load_json_intents(intents)

        self.lemmatizer: WordNetLemmatizer = WordNetLemmatizer()

    def load_json_intents(self, intents: str) -> None:
        self.intents: dict = json.loads(open(self.path_extension + intents, encoding=self.json_encoding).read())

    def train_model(self, epoch_times: int = 1000) -> None:

        self.words: list = []
        self.classes: list = []
        documents: list = []
        ignore_letters: list = ['!', '?', ',', '.']

        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                word: list[str] = nltk.word_tokenize(pattern)
                self.words.extend(word)
                documents.append((word, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        self.words = [self.lemmatizer.lemmatize(w.lower()) for w in self.words if w not in ignore_letters]
        self.words = sorted(list(set(self.words)))

        self.classes = sorted(list(set(self.classes)))
        training: ndarray = []
        output_empty: list = [0] * len(self.classes)

        for doc in documents:
            bag: list = []
            word_patterns = doc[0]
            word_patterns = [self.lemmatizer.lemmatize(word.lower()) for word in word_patterns]
            for word in self.words:
                bag.append(1) if word in word_patterns else bag.append(0)

            output_row: list = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training)

        train_x: list = list(training[:, 0])
        train_y: list = list(training[:, 1])

        self.model = Sequential()
        self.prepare_model(1024, 64, 0.5)
        self.model.add(Dense(len(train_y[0]), activation='softmax'))

        validation_data = self.load_validataion_data()

        adelta = Adadelta(learning_rate=0.1, rho=0.95, epsilon=1e-8, name='Adadelta')
        sgd = SGD(learning_rate=0.0025, decay=1e-8, momentum=0.95, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer=adelta, metrics=['accuracy'])
        self.hist = self.model.fit(np.array(train_x), np.array(train_y), epochs=epoch_times,
                                   validation_data=validation_data, batch_size=15, shuffle=True,
                                   steps_per_epoch=50, verbose=1, workers=15)
        # self.show_result(self.hist)

    def prepare_model(self, max: int, min: int, steps: int) -> None:
        actual: int = max
        while actual > min:
            self.model.add(Dense(actual, activation='relu'))
            self.model.add(Dropout(steps))
            actual -= actual * steps

    def show_result(self, history_dict):
        acc = history_dict['accuracy']
        val_acc = history_dict['val_accuracy']
        loss = history_dict['loss']
        val_loss = history_dict['val_loss']

        epochs = range(1, len(acc) + 1)

        # "bo" is for "blue dot"
        plt.plot(epochs, acc, 'bo', label='Training acc')
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()

        plt.show()

    def save_model(self, model_name: str = None) -> None:
        if model_name is None:
            self.model.save("{}.h5".format(self.model_name), self.hist)
            pickle.dump(self.words, open('{}{}_words.pkl'.format(self.path_extension, self.model_name), 'wb'))
            pickle.dump(self.classes, open('{}{}_classes.pkl'.format(self.path_extension, self.model_name), 'wb'))
        else:
            self.model.save("{}.h5".format(model_name), self.hist)
            pickle.dump(self.words, open('{}{}_words.pkl'.format(self.path_extension, model_name), 'wb'))
            pickle.dump(self.classes, open('{}{}_classes.pkl'.format(self.path_extension, model_name), 'wb'))

    def load_model(self, model_name: str = None) -> None:
        if model_name is None:
            self.words = pickle.load(open('{}{}_words.pkl'.format(self.path_extension, self.model_name), 'rb'))
            self.classes = pickle.load(open('{}{}_classes.pkl'.format(self.path_extension, self.model_name), 'rb'))
            self.model = load_model('{}{}.h5'.format(self.path_extension, self.model_name), compile=True)
            # self.model = tensorflow.lite.Interpreter('{}{}.h5'.format(self.path_extension, self.model_name))
            # self.model.allocate_tensors()
        else:
            self.words = pickle.load(open('{}{}_words.pkl'.format(self.path_extension, model_name), 'rb'))
            self.classes = pickle.load(open('{}{}_classes.pkl'.format(self.path_extension, model_name), 'rb'))
            self.model = load_model('{}{}.h5'.format(self.path_extension, model_name), compile=True)

    def load_validataion_data(self) -> Tuple[list, list]:
        with open(self.path_extension + "validation_data.json", "r") as validation_file:
            validation_data: dict = json.load(validation_file)
            training: list = []
            output_empty: list = [0] * len(self.classes)
            documents: list = []

            for pattern in validation_data["validation"]:
                word = nltk.word_tokenize(pattern)
                documents.append((word, validation_data["validation"][pattern]))
            for doc in documents:
                bag = []
                word_patterns = doc[0]
                word_patterns = [self.lemmatizer.lemmatize(word.lower()) for word in word_patterns]
                for word in self.words:
                    bag.append(1) if word in word_patterns else bag.append(0)

                output_row = list(output_empty)
                output_row[self.classes.index(doc[1])] = 1
                training.append([bag, output_row])

            random.shuffle(training)
            training = np.array(training)
            train_x = list(training[:, 0])
            train_y = list(training[:, 1])
            return (train_x, train_y)

    def _clean_up_sentence(self, sentence: str) -> list:
        sentence_words: list = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    def _bag_of_words(self, sentence: str, words: list) -> list:
        sentence_words = self._clean_up_sentence(sentence)
        bag = [0] * len(words)
        for s in sentence_words:
            for i, word in enumerate(words):
                if word == s:
                    bag[i] = 1

        return np.array(bag)

    def _predict_class(self, sentence: str) -> list:
        p: list = self._bag_of_words(sentence, self.words)
        res = self.model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.1
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': r[1]})
        return return_list

    def _get_response(self, ints: list, intents_json) -> str:
        try:
            tag = ints[0]['intent']
            list_of_intents = intents_json['intents']
            for i in list_of_intents:
                if i['tag'] == tag:
                    result = random.choice(i['responses'])
                    break
        except IndexError:
            result = "I don't understand!"
        return result

    def request(self, message: str) -> dict | str:
        for item in message:
            if item not in self.words:
                message.replace(item, '*')
        ints: dict = self._predict_class(message)
        if not ints:
            raise Exception('Couldn\'n find a matching entry')
        if ints[0]['probability'] < 0.5:
            return None
        if ints[0]['intent'] in self.intent_methods.keys():
            return {"module": self.intent_methods.get(ints[0]['intent']), "intent": ints[0]['intent']}
        else:
            return self._get_response(ints, self.intents)

    def test_request(self, message: str) -> dict | str:
        ints: dict = self._predict_class(message)
        # print(f'{message} : {ints[0]}')
        return ints[0]['intent']