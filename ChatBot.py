# Useful libraries
import sys
import os
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn


# Library used to build the chatbot
from programy.clients.embed.basic import EmbeddedDataFileBot

# the default responses if no pattern matches
default_patterns = ["Can you repeat, please?", "I don’t understand", "Can you say that more clearly?"] 

# possible words that make sense to be substituted, for efficiency purpose
noun_list = ["tour", "art", "discipline", "city", "lodging", "sightseeing", "excursion", "abroad", "guide"]
verb_list = ["organize", "book", "suggest", "rate"]

def main():

    # define folders containing the main files
    files = {'aiml': ['y-bot/storage/categories'],
         'learnf': ['y-bot/storage/categories/learnf'],
         'properties': 'y-bot/storage/properties/properties.txt',
         'defaults': 'y-bot/storage/properties/defaults.txt',
         'sets': ['y-bot/storage/sets'],
         'maps': ['y-bot/storage/maps'],
         'rdfs': ['y-bot/storage/rdfs'],
         'denormals': 'y-bot/storage/lookups/denormal.txt',
         'normals': 'y-bot/storage/lookups/normal.txt',
         'genders': 'y-bot/storage/lookups/gender.txt',
         'persons': 'y-bot/storage/lookups/person.txt',
         'person2s': 'y-bot/storage/lookups/person2.txt',
         'regexes': 'y-bot/storage/regex/regex-templates.txt',
         'spellings': 'y-bot/storage/spelling/corpus.txt',
         'preprocessors': 'y-bot/storage/processing/preprocessors.conf',
         'postprocessors': 'y-bot/storage/processing/postprocessors.conf',
         'postquestionprocessors': 'y-bot/storage/processing/postquestionprocessors.conf'
         }


    chatbot = EmbeddedDataFileBot(files, defaults=True) 


    while True:
        message = input("> ")
        response = chatbot.ask_question(message)
    
        # if response is not None
        if response: 

            # if no pattern matches it may be applied a learning
            if response in default_patterns: 
        
                learned = learn_pattern(chatbot, message)

                # if a new pattern is learned then retrieve the new response of that pattern
                if learned: 
                    response = chatbot.ask_question(message)

            # in any case print the response 
            print("> Guido: {}".format(response))

        # message to exit
        if message == "quit":
            break



def learn_pattern(chatbot, message):

    # categories in order to be able to learn
    synonym_string = " is synonym of "
    hyponym_string = " is hyponym of "
    hypernym_string = " is hypernym of "

    # tokenizer that discard punctuation and white spaces
    tokenizer = RegexpTokenizer(r'\w+')
    words_list = tokenizer.tokenize(message)

    # find synonym
    is_syn, new_message = find_lexical_relation(words_list, message, "synonym")

    # learn the new pattern and return 
    if is_syn:
        # first check that such a pattern already exist
        new_response = chatbot.ask_question(new_message)

        # the new category can be learned
        if new_response not in default_patterns:
            chatbot.ask_question(message + synonym_string + new_message)
            return True
        
    # find hyponym
    is_hypo, new_message = find_lexical_relation(words_list, message, "hyponym")

    # learn the new pattern and return 
    if is_hypo:
        # first check that such a pattern already exist
        new_response = chatbot.ask_question(new_message)

        # the new category can be learned
        if new_response not in default_patterns:
            chatbot.ask_question(message + hyponym_string + new_message)
            return True

    # find hypernym
    is_hyper, new_message = find_lexical_relation(words_list, message, "hypernym")

    # learn the new pattern and return 
    if is_hyper:
        # first check that such a pattern already exist
        new_response = chatbot.ask_question(new_message)

        # the new category can be learned
        if new_response not in default_patterns:
            chatbot.ask_question(message + hypernym_string + new_message)
            return True

    return False


def find_lexical_relation(words_list, message, type="synonym"):


    # Lemming using WordNet 
    lemmatizer = WordNetLemmatizer()

    # Lemming words as Nouns
    words_noun_list = Lemmatization(lemmatizer, words_list, "n")

    # Lemmin words as Verbs
    words_verb_list = Lemmatization(lemmatizer, words_list, "v")

    # converts all characters into lowercase
    message = message.lower()

    # Lexical relation 
    
    # find relation for Nouns
    is_rel, new_message = lexical_relation(words_noun_list, noun_list, message, wn.NOUN, type)

    if is_rel:
        return True, new_message

    # find relation for Verbs
    is_rel, new_message = lexical_relation(words_verb_list, verb_list, message, wn.VERB, type)

    if is_rel:
        return True, new_message


    return False, ""


# return True is there is a lexical relation and return also the sentence the chatbot is already able to recognise
def lexical_relation(words_list, baseline_words, message, key = wn.NOUN, type="synonym" ):


    # initialized so that if no correspondence are found, properly values are returned
    rel_found = False

    for word in words_list:
    
        # check if "word" is related with any word of interest in baseline_words
        
        for baseline in baseline_words:
            synset_list = wn.synsets(baseline, pos=key)

            # check if there is a synset containing both relating "word" and "baseline"
            for synset in synset_list:

                if type == "synonym":
                    replaced , message = replace_synonymy(word, baseline, message, synset)

                if type == "hyponym":
                    replaced , message = replace_hyponymy(word, baseline, message, synset)

                if type == "hypernym":
                    replaced , message = replace_hypernym(word, baseline, message, synset)

                if replaced:
                    rel_found = True

    if rel_found:
        return rel_found, message
    else:
        return rel_found, ""
  



def replace_synonymy(word, baseline, message, synset):

    rel_found = False

    if word in synset.lemma_names():
    
        # relation found
        rel_found = True

        # replace all instances of "word" with "baseline"
        message = message.replace(word, baseline, message)

    # if no correspondence found it may be a collocation
    if not rel_found:
        for lemma in synset.lemma_names():

            is_in = isThere_collocation(word, lemma, message)

            if is_in:

                # replace all instances of "word" with "baseline"
                message = message.replace(lemma, baseline, message)

                rel_found = True

    return rel_found, message

def replace_hyponymy(word, baseline, message, synset):

    rel_found = False

    hypos = synset.hyponyms()
    for hypo in hypos:

        if word in hypo.lemma_names():

            # relation found
            rel_found = True

            # replace all instances of "word" with "baseline"
            message = message.replace(word, baseline, message)
                    
    # if no correspondence found it may be a collocation
    if not rel_found:
        for lemma in hypo.lemma_names():

            is_in = isThere_collocation(word, lemma, message)

            if is_in:

                # replace all instances of "word" with "baseline"
                message = message.replace(lemma, baseline, message)
                
                rel_found = True

    return rel_found, message

def replace_hypernym(word, baseline, message, synset):

    rel_found = False

    hypers = synset.hypernyms()
    for hyper in hypers:

        if word in hyper.lemma_names():

            # relation found
            rel_found = True

            # replace all instances of "word" with "baseline"
            message = message.replace(word, baseline, message)

    # if no correspondence found it may be a collocation
    if not rel_found:
        for lemma in hyper.lemma_names():

            is_in = isThere_collocation(word, lemma, message)

            if is_in:

                # replace all instances of "word" with "baseline"
                message = message.replace(lemma, baseline, message)

                rel_found = True

    return rel_found, message

def Lemmatization(lemmatizer, word_list, pos):

    return [lemmatizer.lemmatize(word, pos = pos) for word in word_list]

def isThere_collocation(word, baseline, message):

    # in the corpus the collocations are separated by _
    if("_" in baseline):

        baseline = baseline.replace("_", " ")

        # the collocation is in the message
        if word in baseline and baseline in message:

            return True, message

    return False, message

# run main
if __name__ == "__main__":
    main()


