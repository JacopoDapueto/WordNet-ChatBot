# load my own library
from chatbot import *

# Library used to build the chatbot
from programy.clients.embed.configfile import EmbeddedConfigFileBot


quit_pattern = "Ok, bye bye!"

def main():

    chatbot = EmbeddedConfigFileBot("y-bot/config.yaml")

    # use a user for testing
    client_context = chatbot.create_client_context("testuser")

    print("> Guido: {}".format(chatbot.process_question(client_context, "Hi")))

    while True:
        message = input("> You: ")
        response = chatbot.process_question(client_context, message)
    
        # if response is not None
        if response: 

            # if no pattern matches it may be applied a learning
            if not_recognise(response): 
                
                learned = learn_pattern(chatbot, client_context, message)

                # if a new pattern is learned then retrieve the new response of that pattern
                if learned: 
                    
                    response = chatbot.process_question(client_context, message)

            # in any case print the response 
            print("> Guido: {}".format(response))

        # message to exit
        if response == quit_pattern:
            break




# run main
if __name__ == "__main__":
    main()

