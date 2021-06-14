import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

import aiml

import sys
import os

noun_list = ["tour", "art", "lodging", "book", "information", "architecture"]

print("_" in "franco_pino")
print("FRANCO_pinO".replace("_", " "))

print("pino pano" in "pino pano pono", "pino pono" in "pino pano pono")

print("living" in "living_accomodation")

# Lemming using WordNet 
lemmatizer = WordNetLemmatizer()

for word in noun_list: 

    lemmatizer.lemmatize(word, pos = "n")

    print()
    print()
    print(word)
    print()

    syn = wn.synsets(word, pos=wn.NOUN)

    print("Synsets")

    for s in syn:

        print(s.lemma_names())


    print()
    print("Hypernyms")
    
    print([s.hypernyms() for s in syn])

    print()
    print("Hyponyms")
    print([ s.hyponyms() for s in syn])