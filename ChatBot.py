
# Useful libraries
import sys
import os
import nltk
import string
from nltk.grammar import nonterminals
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

# Load utils
from utils import *



def learn_pattern(chatbot, client_context, message):

    # tokenizer that discard punctuation and white spaces
    tokenizer = RegexpTokenizer(r'\w+')
    words_list = tokenizer.tokenize(message)


    # find synonym for each word

    for word in words_list:
        is_syn, base_message = find_lexical_relation(word, message, Relations.SYNONYM)

        # learn the new pattern and return 
        if is_syn:
            learned = can_be_learned(chatbot, client_context, message, base_message, Relations.synonym_string)

            if learned:
                return True
        
    # find hyponym for each word
    for word in words_list:
        is_hypo, base_message = find_lexical_relation(word, message, Relations.HYPONYM)

        # learn the new pattern and return 
        if is_hypo:
            learned = can_be_learned(chatbot, client_context, message, base_message, Relations.hyponym_string)

            if learned:
                return True

    # find hypernym for each word
    for word in words_list:
        is_hyper, base_message = find_lexical_relation(word, message, Relations.HYPERNYM)

        # learn the new pattern and return 
        if is_hyper:
            learned = can_be_learned(chatbot, client_context, message, base_message, Relations.hypernym_string)

            if learned:
                return True

    return False

def can_be_learned(chatbot, client_context, message, base_message, relation):

    # first check that such a pattern already exist
    new_response = chatbot.process_question(client_context, base_message)

    # the new category can be learned
    if not not_recognise(new_response):

        # removing punctuation from the messages
        message = message.translate(dict((ord(char), None) for char in string.punctuation))
        base_message = base_message.translate(dict((ord(char), None) for char in string.punctuation))
        #print(message)

        # disable splitting to avoid erroneous pattern to be learned
        chatbot.process_question(client_context, CategoriesOfInterest.disable_splitting)

        # learnf the category: message will be reduced to base_message
        chatbot.process_question(client_context, "relation " + message + relation + base_message )

        # enable sentence splitting again
        chatbot.process_question(client_context, CategoriesOfInterest.enable_splitting)
        return True

    return False


def find_lexical_relation(word, message, type=Relations.SYNONYM):

    # Lemming words as Nouns
    word_noun = Lemmatization_word(word, "n")

    # Lemmin words as Verbs
    word_verb = Lemmatization_word(word, "v")

    # converts all characters into lowercase
    message = message.lower()

    # Lexical relation 
    
    # find relation for Nouns
    is_rel, new_message = lexical_relation(word_noun, TermsOfInterest.noun_list, message, wn.NOUN, type)

    if is_rel:
        return True, new_message

    # find relation for Verbs
    is_rel, new_message = lexical_relation(word_verb, TermsOfInterest.verb_list, message, wn.VERB, type)

    if is_rel:
        return True, new_message


    return False, ""


# return True is there is a lexical relation and return also the sentence the chatbot is already able to recognise
def lexical_relation(word, baseline_words, message, key = wn.NOUN, type=Relations.SYNONYM ):

    
    # check if "word" is related with any word of interest in baseline_words
    for baseline in baseline_words:

        lemma = Lemmatization_word(baseline, key)

        synset_list = wn.synsets(lemma, pos=key)


        # check if there is a synset containing both relating "word" and "baseline"
        for synset in synset_list:

            if type == Relations.SYNONYM:
                replaced , new_message = replace_synonymy(word, baseline, message, synset)

            if type == Relations.HYPONYM:
                replaced , new_message = replace_hyponymy(word, baseline, message, synset)

            if type == Relations.HYPERNYM:
                replaced , new_message = replace_hypernym(word, baseline, message, synset)

            if replaced:

                return True, new_message

    
    return False, ""
  
def replace_synonymy(word, baseline, message, synset):

    if word in synset.lemma_names():

        # replace all instances of "word" with "baseline"
        new_message = message.replace(word, baseline)

        return True, new_message

    # if no correspondence found it may be a collocation
    replaced, new_message = replace_collocation(synset.lemma_names(), word, baseline, message)

    if replaced:
        return True, new_message

    return False, ""

def replace_hyponymy(word, baseline, message, synset):

    hypos = synset.hyponyms()
    for hypo in hypos:

        if word in hypo.lemma_names():

            # replace all instances of "word" with "baseline"
            new_message = message.replace(word, baseline)

            return True, new_message
                    
    # if no correspondence found it may be a collocation
    for hypo in hypos:
       replaced, new_message = replace_collocation(hypo.lemma_names(), word, baseline, message)

       if replaced:
            return True, new_message

    return False, ""

def replace_hypernym(word, baseline, message, synset):

    hypers = synset.hypernyms()
    for hyper in hypers:

        if word in hyper.lemma_names():

            # replace all instances of "word" with "baseline"
            new_message = message.replace(word, baseline)

            return True, new_message

    # if no correspondence found it may be a collocation
    for hyper in hypers:
        replaced, new_message = replace_collocation(hyper.lemma_names(), word, baseline, message)

        if replaced:
            return True, new_message

    return False, ""

def Lemmatization_list(word_list, pos):

    # Lemming using WordNet 
    lemmatizer = WordNetLemmatizer()

    return [lemmatizer.lemmatize(word, pos = pos) for word in word_list]


def Lemmatization_word(word, pos):

    # Lemming using WordNet 
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word, pos = pos)


def replace_collocation(lemma_names, word, baseline, message):

    for lemma in lemma_names:
    
            is_in = isThere_collocation(word, lemma, message)

            if is_in:

                # replace all instances of "word" with "baseline"
                new_message = message.replace(lemma.replace("_", " ") , baseline)

                return True, new_message

    return False, ""


# return if the message is not recognise by the chatbot as something meaningful
def not_recognise(response):

    return (response in CategoriesOfInterest.default_patterns or CategoriesOfInterest.interest_pattern in response)


# return if in the message there is a collocation present in the synset
def isThere_collocation(word, baseline, message):


    # in the corpus the collocations are separated by _
    if("_" in baseline):

        baseline = baseline.replace("_", " ")    

        # the collocation is in the message
        if word in baseline and baseline in message:
            return True

    return False
    






