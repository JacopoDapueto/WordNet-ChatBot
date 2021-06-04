import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

import aiml

import sys
import os

noun_list = ["tour", "art", "lodging", "book"]

print("_" in "franco_pino")
print("FRANCO_pinO".replace("_", " "))

# Lemming using WordNet 
lemmatizer = WordNetLemmatizer()

for word in noun_list: 

    lemmatizer.lemmatize(word, pos = "v")

    print()
    print()
    print(word)
    print()

    syn = wn.synsets(word, pos=wn.VERB)

    print("Synsets")
    print(syn)


    print()
    print("Hypernyms")
    
    print([s.hypernyms() for s in syn])

    print()
    print("Hyponyms")
    print([s.hyponyms() for s in syn])