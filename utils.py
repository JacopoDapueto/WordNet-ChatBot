
class TermsOfInterest:
    
    # possible words that make sense to be substituted, for efficiency purpose
    noun_list = ["tour", "art", "discipline", "city", "lodging", "sightseeing", "excursion", "guide", "tariff", "reservation", "informations", "confirmation","hi", "goodbye"]
    verb_list = ["organize", "book", "suggest", "rate", "lead", "receive", "cancel", "go", "love", "pay"] 
    adj_list = ["abroad", "interested"]


class Relations:

    # categories in order to be able to learn
    synonym_string = " is synonym of "
    hyponym_string = " is hyponym of "
    hypernym_string = " is hypernym of "


    SYNONYM = "synonym"
    HYPONYM = "hyponym"
    HYPERNYM = "hypernym"


class CategoriesOfInterest:

     # the default responses if no pattern matches
    default_patterns = ["Can you repeat, please?", "I don’t understand.", "Can you say that more clearly?" ] 
    interest_pattern = "It's a pity we've no tours regarding"

    # categories to enable/disable sentence splitting
    enable_splitting = "set the splitter on"
    disable_splitting = "set the splitter off"

    # the pattern used to quit the chatbot
    quit_pattern = "Ok, bye bye!"
