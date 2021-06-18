
class TermsOfInterest:
    # Ground terms

    # possible words that make sense to be substituted, for efficiency purpose
    noun_list = ["tour", "art", "discipline", "city", "lodging", "sightseeing", "excursion", "guide", "tariff", "reservation", "information", "confirmation", "architecture", "service", "archeology", "explorer", "nature", "literature", "history","hi", "goodbye"]
    verb_list = ["organize", "book", "suggest", "rate", "lead", "receive", "cancel", "go", "love", "pay", "choose", "like", "help", "find", "provide", "ready", "contact", "join", "leave", "design"] 
    adj_list = ["abroad", "interested", "available"]


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

# return if the message is not recognise by the chatbot as something meaningful
def not_recognise(response):

    return (response in CategoriesOfInterest.default_patterns or CategoriesOfInterest.interest_pattern in response)

# return if the chatbot recognize the response 
def can_be_learned(response):

    return response not in CategoriesOfInterest.default_patterns
