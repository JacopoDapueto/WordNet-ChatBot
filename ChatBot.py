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
noun_list = ["tour", "art", "discipline", "city", "lodging", "sightseeing", "excursion"]
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

    # Synonym relation
    if type == "synonym":

        # find synonym for Nouns
        is_syn, new_message = synonym_relation(words_noun_list, noun_list, message)

        if is_syn:
            return True, new_message

        # find synonym for Verbs
        is_syn, new_message = synonym_relation(words_verb_list, verb_list, message, wn.VERB)

        if is_syn:
            return True, new_message

     # Hyponymy relation
    if type == "hyponym":

        # find hyponym for Noun
        is_hypo, new_message = hyponym_relation(words_noun_list, noun_list, message)

        if is_hypo:
            return True, new_message

        # find hyponym for Verb
        is_hypo, new_message = hyponym_relation(words_verb_list, verb_list, message, wn.VERB)

        if is_hypo:
            return True, new_message


     # Synonym relation
    if type == "hypernym":

        # find hypernym for Noun
        is_hyper, new_message = hypernym_relation(words_noun_list, noun_list, message)

        if is_hyper:
            return True, new_message

        # find hypernym for Verb
        is_hyper, new_message = hypernym_relation(words_verb_list, verb_list, message, wn.VERB)

        if is_hyper:
            return True, new_message


    return False, ""


# return True is there is a synonym relation and return also the sentence the chatbot is already able to recognise
def synonym_relation(words_list, baseline_words, message, key = wn.NOUN):


    # initialized so that if no correspondence are found, properly values are returned
    rel_found = False

    for word in words_list:
    
        # check if "word" is synonym of any word of interest in baseline_words
        
        for baseline in baseline_words:
            synset_list = wn.synsets(baseline, pos=key)

            # check if there is a synset containing both it means they have same meaning
            for synset in synset_list:
                if word in synset.lemma_names():

                    # relation found
                    rel_found = True
                    
                    # replace all instances of "word" with "baseline"
                    message = message.replace(word, baseline)
            

    if rel_found:
        return rel_found, message
    else:
        return rel_found, ""
    
def hyponym_relation(words_list, baseline_words, message, key = wn.NOUN):
    

    # initialized so that if no correspondence are found, properly values are returned
    rel_found = False

    for word in words_list:
    
        # check if "word" is synonym of any word of interest in baseline_words
        
        for baseline in baseline_words:
            synset_list = wn.synsets(baseline, pos=key)

            # check if there is a synset containing both it means they have same meaning
            for synset in synset_list:
                hypos = synset.hyponyms()
                for hypo in hypos:

                    if word in hypo.lemma_names():

                        # relation found
                        rel_found = True
                    
                        # replace all instances of "word" with "baseline"
                        message = message.replace(word, baseline)


    if rel_found:
        return rel_found, message
    else:
        return rel_found, ""

def hypernym_relation(words_list, baseline_words, message, key = wn.NOUN):

    # initialized so that if no correspondence are found, properly values are returned
    rel_found = False

    for word in words_list:
    
        # check if "word" is synonym of any word of interest in baseline_words
        
        for baseline in baseline_words:
            synset_list = wn.synsets(baseline, pos=key)

            # check if there is a synset containing both it means they have same meaning
            for synset in synset_list:
                hypers = synset.hypernyms()
                for hyper in hypers:

                    if word in hyper.lemma_names():

                        # relation found
                        rel_found = True
                    
                        # replace all instances of "word" with "baseline"
                        message = message.replace(word, baseline)


    if rel_found:
        return rel_found, message
    else:
        return rel_found, ""


def Lemmatization(lemmatizer, word_list, pos):

    return [lemmatizer.lemmatize(word, pos = pos) for word in word_list]

# run main
if __name__ == "__main__":
    main()


