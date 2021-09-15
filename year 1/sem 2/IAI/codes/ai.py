from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

from numpy import array, argmax
import tflearn
import tensorflow
import random
import json
from os.path import isfile

# Loading templates
with open("templates.json") as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

# Tokenizing the words
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

def train():
    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]
    # Preparing the data
    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = array(training)
    output = array(output)    
    # tensorflow.compat.v1.reset_default_graph()
    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)
    model = tflearn.DNN(net)
    # Load the model, if not inside, train a model
    if isfile("model.tflearn.meta"):
        model.load("model.tflearn")
        return model

    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn") # saving it
    return model

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return array(bag)


def predict(model, inp):
    results = model.predict([bag_of_words(inp, words)])
    results_index = argmax(results)
    tag = labels[results_index]

    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']

    return (tag, random.choice(responses))

