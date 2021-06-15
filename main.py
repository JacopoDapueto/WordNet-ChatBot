# load my own library
from wn_integration import *
from utils import *

# Library used to build the chatbot
from programy.clients.embed.configfile import EmbeddedConfigFileBot



def main():

    chatbot = EmbeddedConfigFileBot("y-bot/config.yaml")

    # use a user for testing
    client_context = chatbot.create_client_context("testuser")

    print("> Guido: {}".format(chatbot.process_question(client_context, "Hi")))

    while True:

        # get the message from the user and let the chatbot digests it
        message = input("> You: ")

        # split the message and possibily learn new patterns
        split_and_learn_sentences(chatbot, client_context, message)

        # get response from the chatbot
        response = chatbot.process_question(client_context, message)

        if response:
            # in any case print the response 
            print("> Guido: {}".format(response))

        # message to exit
        if response == CategoriesOfInterest.quit_pattern:
            break


# it splits the message according to the splitter of the chatbot 
# and it check if each chunck can be learned as new pattern
def split_and_learn_sentences(chatbot, client_context, message):

    pre_processed_sentence = client_context.bot.pre_process_text(client_context, message, srai=False)

    # split the sentence into smaller sentences according to the punctuation
    senteces_list = client_context.bot.sentence_splitter.split(pre_processed_sentence) 

    for sentence in senteces_list:
        response = chatbot.process_question(client_context, sentence)

         # if response is not None
        if response: 

            # if no pattern matches it may be applied a learning
            if not_recognise(response): 
                
                learn_pattern(chatbot, client_context, sentence)

# run main
if __name__ == "__main__":
    main()

