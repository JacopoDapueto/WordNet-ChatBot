import nltk
from nltk.corpus import wordnet as wn
import aiml

import sys
import os

noun_list = ["tour", "art"]

for word in noun_list: 

    syn = wn.synsets(word, pos=wn.NOUN)

    print("Synsets")
    print(syn)


    print()
    print("Hypernyms")
    
    print(syn.hypernyms())

    print()
    print("Hyponyms")
    print(syn.hyponyms())