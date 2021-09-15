import json
import requests

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tree import Tree

from spellchecker import SpellChecker

from difflib import get_close_matches


# -------------------------------------------------------------------------------------------
# !!! the dict for the symptoms in knowledge base is used as symptomsDict in here !!!
# -------------------------------------------------------------------------------------------


# download these if using it for the first time
'''
nltk.download("stopwords")
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('punkt')
'''

remove = ['eat', 'help', 'consume', 'avoid', 'diet', 'take', 'please', 'follow', 'aid', 'get', 'work', 'give',
          'condition', 'disease', 'illness', 'sickness', 'infection', 'ailment', 'medical',
          'issue', 'problem', 'disorder',
          'food', 'nourishment', 'sustenance', 'substance', 'nutriment', 'nutrition', 'nutrient', 'meal',
          'type', 'method', 'solution', 'patient', 'actually', 'always', 'good', 'best', 'most']
capitalise = ['aids', 'hiv']

spell = SpellChecker()
spell.word_frequency.load_words(['aids', 'cholesterolemia', 'beri', 'crohn', 'oiliness', 'hyperkinesis',
                                 'hyperlipidemia', 'lupuses', 'myopathy', 'dysgeusia', 'parageusia', 'syringoma',
                                 'relux', 'xanthelasma', 'xerophthalmia', 'cheilitis', 'toxicosis', 'meniere',
                                 'miliaria', 'nycatalopia', 'subacute'])  # can put new words into vocabulary
frontLink = "https://wordsapiv1.p.rapidapi.com/words/"
backLink = "/pertainsTo"
headers = {'x-rapidapi-key': "598888eb7bmsh90cec9cd6809f87p1cdf1ajsn82648f4314c5",
           'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"}
lemm = WordNetLemmatizer()

def lemmatize(string):
    return lemm.lemmatize(string)

def scan(rawInput, symptomsDict):
    rawInput = rawInput.casefold()
    rootWordSet = set()
    correctionDict = {}
    possibleSet = set()
    synonymSymptomsDict = {}
    # separating possible conditions
    splitText = rawInput.replace(' andd ', ' , ').replace(' amd ', ' , ').replace(' and ', ' , ').split(',')

    for indivText in splitText:
        # user input and split non-identical words into list
        userText = word_tokenize(indivText)
        userText = list(dict.fromkeys(userText).keys())  # removing duplicates

        # correcting spelling for common words
        misspelled = spell.unknown(userText)  # find those words that may be misspelled
        correctionDictTmp = {}
        for word in misspelled:
            correctionDictTmp[word] = spell.correction(word)  # storing into dict
        for i, word in enumerate(userText):
            if word in correctionDictTmp:
                userText[i] = correctionDictTmp[word]
            if word in capitalise:
                userText[i] = (userText[i]).upper()
        # correctionDict.update(correctionDictTmp)

        # removing stopwords
        stop_words = set(stopwords.words('english'))  # examples of stopwords are 'is, are, in, an, am, his'
        noStopwords = [
            word for word in userText
            if word not in stop_words
        ]

        # lemmatising words
        
        lemmatisedWords = [lemmatize(w) for w in noStopwords]  # changing plural to singular

        for i in lemmatisedWords[:]:
            if i in remove:
                lemmatisedWords.remove(i)

        # tagging words to their own type
        taggedWords = nltk.pos_tag(lemmatisedWords)

        if taggedWords:
            # chunking the words
            grammar = "NP: {<NNP>*<JJ>*<RB>*<DT>*<VB>*<VBN>*<IN>*<VBD>*<VBP>*<VBZ>*<VBG>*<NNS>*<NN>*}"
            chunkParser = nltk.RegexpParser(grammar)
            chunked = chunkParser.parse(taggedWords)

            possible = []
            current = []
            for i in chunked:
                if type(i) == Tree:
                    current.append(" ".join([token for token, pos in i.leaves()]))
                if current:
                    named_entity = " ".join(current)
                    if named_entity not in possible:
                        possible.append(named_entity)
                        current = []

            originalWords = list(correctionDictTmp.keys())
            fixedWords = list(correctionDictTmp.values())

            for i in possible:
                # adding possible symptoms into possibleSet
                possibleSet.add(i)

                # adding synonym for whole term of symptoms into synonymSymptomsDict
                if i not in synonymSymptomsDict:
                    synonymSymptomsDict[i] = get_close_matches(i, symptomsDict, 3, 0.1)

                # adding corrected words into correctionDict
                # also adding root words into rootWordSet
                # also adding synonym for individual words of symptoms into synonymSymptomsDict
                checkCorrection = i.split(" ")
                for j in checkCorrection:
                    if j in fixedWords:
                        if j not in correctionDict:
                            # inserting corrected symptom's word into correctionDict
                            correctionDict[originalWords[fixedWords.index(j)]] = j
                    if j not in rootWordSet:
                        url = frontLink + j + backLink
                        response = requests.request("GET", url, headers=headers)
                        if response.status_code == 200:
                            RootWord = json.loads(response.text)
                            if RootWord["pertainsTo"]:
                                rootWordSet.add(RootWord["pertainsTo"][0])
                    if j not in synonymSymptomsDict:
                        synonymSymptomsDict[j] = get_close_matches(i, symptomsDict, 3, 0.1)


    # possibleSet contains all possible symptoms  (eg: ['diabetes', high blood pressure'])
    # print(f'\nPossible symptoms: {possibleSet}')

    # rootWordSet contains all root words of possible symptoms  (eg: {'diabetes'})
    # print(f'\nRoot words: {rootWordSet}')

    # synonymSymptomsDict contains all synonyms of possible symptoms (eg: {'diabetes'})
    # print(f'\nSynonym symptoms: {synonymSymptomsDict}')

    # correctionDict contains all corrected words of possible symptoms  (eg: {'diabeticc': 'diabetic'})
    # print(f'\ncorrected words: {correctionDict}')
    return (possibleSet, rootWordSet, synonymSymptomsDict, correctionDict)
