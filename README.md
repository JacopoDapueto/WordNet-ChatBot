# ChatBot

Project of NLP. Implementation of a chatbot with capabilities of recognizing lexical relations thanks to the [Wordnet](https://wordnet.princeton.edu/) database.
It is implemented in **AIML 2.0** that thanks to its semplicity it’s possible to define a limited number of patterns the software is able to recognize and to answer.
 
The chatbot is supposed to work in the touristic domain as support to a website of a tour sharing community. it is a service where users ( of two kind: *guides* and *explorers*) can design and propose guided tours and partecipate to them with strangers in order share the costs and to save money. The software has the ability to answer to frequently asked questions of how the businness works, explain the rule of the game and it also tries to help the user in finding the most suitable activities for them. Such actitivities are tagged with the locations where they take place and with the involved topics. Such tags are integrated as two AIML sets.

It is able to learn lexical relations of a finite set of words that play a role in the domain of interest and that are explicitly stated in  the patterns, moreover They are also divided according to their grammar category (the lists are defined in [util.py](utils.py)).


The python implementation is provided by [program-y](https://github.com/keiffster/program-y).

### Requirements
```
pip3 install -r requirements.txt
```

```
python3 -m nltk.downloader wordnet 
```

```
python3 main.py 
```
