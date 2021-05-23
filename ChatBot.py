# Useful libraries
import nltk
import aiml
import sys
import os

# Library used to build the chatbot
from programy.clients.embed.basic import EmbeddedDataFileBot

# define folders containing the main files
files = {'aiml': ['y-bot/storage/categories'],
         'learnf': ['y-bot/storage/learnf'],
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

bot = EmbeddedDataFileBot(files)

while True:

    message = input("> ")
    response = bot.ask_question(message)
    if response: 
        print("> Guido: {}".format(response))
    
    if message == "quit":
        break