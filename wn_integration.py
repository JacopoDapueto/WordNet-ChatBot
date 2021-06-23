
# Useful libraries
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
        learned, base_message = find_lexical_relation(chatbot, client_context, word, message, Relations.SYNONYM)

        if learned:
            return True
        
    # find hyponym for each word
    for word in words_list:
        learned, base_message = find_lexical_relation(chatbot, client_context, word, message, Relations.HYPONYM)

        if learned:
            return True

    # find hypernym for each word
    for word in words_list:
        learned, base_message = find_lexical_relation(chatbot, client_context, word, message, Relations.HYPERNYM)

        if learned:
            return True

    return False


# return if it find a lexical relation for one of grammar category
def find_lexical_relation(chatbot, client_context, word, message, type=Relations.SYNONYM):

    # Lemming words as Nouns
    word_noun = Lemmatization_word(word, "n")

    # Lemmin words as Verbs
    word_verb = Lemmatization_word(word, "v")

    # Lemmin words as Adj
    word_adj = Lemmatization_word(word, "a")

    # converts all characters into lowercase
    message = message.lower()

    # Lexical relations
    
    # find relation for Nouns
    learned, new_message = lexical_relation(word, word_noun, TermsOfInterest.noun_list , chatbot, client_context , message, wn.NOUN, type)

    if learned:
        return True, new_message

    # find relation for Verbs
    learned, new_message = lexical_relation(word, word_verb, TermsOfInterest.verb_list, chatbot, client_context ,message, wn.VERB, type)

    if learned:
        return True, new_message

    # find relation for Verbs
    learned, new_message = lexical_relation(word, word_adj, TermsOfInterest.adj_list, chatbot, client_context, message, wn.ADJ, type)

    if learned:
        return True, new_message

    return False, ""


# return True is there is a lexical relation and return also the sentence the chatbot is already able to recognise
def lexical_relation(word, word_lemm, baseline_words, chatbot, client_context , message, key = wn.NOUN, type=Relations.SYNONYM ):

    
    # check if "word" is related with any word of interest in baseline_words
    for baseline in baseline_words:

        lemma = Lemmatization_word(baseline, key)

        synset_list = wn.synsets(lemma, pos=key)


        # check if there is a synset containing both relating "word" and "baseline"
        for synset in synset_list:


            if type == Relations.SYNONYM:
                relation = Relations.synonym_string
                replaced , new_message = replace_synonymy(word, word_lemm, baseline, message, synset)

            if type == Relations.HYPONYM:
                relation = Relations.hyponym_string

                replaced , new_message = replace_hyponymy(word,  word_lemm, baseline, message, synset)

            if type == Relations.HYPERNYM:
                relation = Relations.hypernym_string
                replaced , new_message = replace_hypernym(word,  word_lemm, baseline, message, synset)

            if replaced:
                
                learned = is_learned(chatbot, client_context, message, new_message, relation)

                if learned:
                    return True, new_message

    
    return False, ""

    # return if the sentence is learned,and perform the learning
def is_learned(chatbot, client_context, message, base_message, relation):

    # first check that such a pattern already exist
    new_response = chatbot.process_question(client_context, base_message)

    # the new category can be learned
    if can_be_learned(new_response):

        # disable splitting to avoid erroneous pattern to be learned
        chatbot.process_question(client_context, CategoriesOfInterest.disable_splitting)

        # learnf the category: message will be reduced to base_message
        chatbot.process_question(client_context, "relation " + message + relation + base_message )

        # enable sentence splitting again
        chatbot.process_question(client_context, CategoriesOfInterest.enable_splitting)
        return True

    return False

  

# substitute the word in the message with its synonym 
def replace_synonymy(word, word_lemm, baseline, message, synset):

    if word_lemm in synset.lemma_names():

        # replace all instances of "word" with "baseline"
        new_message = message.replace(word, baseline)

        return True, new_message

    # if no correspondence found it may be a collocation
    replaced, new_message = replace_collocation(synset.lemma_names(), word, word_lemm, baseline, message)

    
    if replaced:

        return True, new_message

    return False, ""

# substitute the word in the message with its hyponym 
def replace_hyponymy(word, word_lemm, baseline, message, synset):

    hypos = synset.hyponyms()
    for hypo in hypos:

        if word_lemm in hypo.lemma_names():

            # replace all instances of "word" with "baseline"
            new_message = message.replace(word, baseline)

            return True, new_message
                    
    # if no correspondence found it may be a collocation
    for hypo in hypos:
       replaced, new_message = replace_collocation(hypo.lemma_names(), word, word_lemm, baseline, message)

       
       if replaced: 
            return True, new_message

    return False, ""

# substitute the word in the message with its hypernym 
def replace_hypernym(word, word_lemm, baseline, message, synset):

    hypers = synset.hypernyms()
    for hyper in hypers:

        if word_lemm in hyper.lemma_names():

            # replace all instances of "word" with "baseline"
            new_message = message.replace(word, baseline)

            return True, new_message

    # if no correspondence found it may be a collocation
    for hyper in hypers:
        replaced, new_message = replace_collocation(hyper.lemma_names(), word, word_lemm, baseline, message)

        if replaced:
            return True, new_message

    return False, ""

# return a list of lemmatized words
def Lemmatization_list(word_list, pos):

    # Lemming using WordNet 
    lemmatizer = WordNetLemmatizer()

    return [lemmatizer.lemmatize(word, pos = pos) for word in word_list]

# lemming a single word
def Lemmatization_word(word, pos):

    # Lemming using WordNet 
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word, pos = pos)

# it find and replace a collocation in the message, if any
def replace_collocation(lemma_names, word, word_lemm, baseline, message):

    for lemma in lemma_names:
    
            is_in = isThere_collocation(word, lemma, message)

            if is_in:

                # prepare  the collocation 
                lem = lemma.replace("_", " ")
                lem = lem.replace(word_lemm, word)
                # replace all instances of "word" with "baseline"
                new_message = message.replace( lem, baseline)

                return True, new_message

    return False, ""



# return if in the message there is a collocation present in the synset
def isThere_collocation(word, baseline, message):


    # in the corpus the collocations are separated by _
    if("_" in baseline):

        baseline = baseline.replace("_", " ")    

        # the collocation is in the message
        if word in baseline and baseline in message:
            return True

    return False
    






