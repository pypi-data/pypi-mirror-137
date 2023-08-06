"""
Utility functions, used primarily for
work tokenize process

:author: 
:date: 
:organization: 
"""

import re
import nltk
from nltk.stem import PorterStemmer
#from nltk.corpus import stopwords

ps = PorterStemmer()
#stopwords = set(stopwords.words('english'))



def clean(text):
    return re.sub(r'[^a-zA-Z0-9\-]', ' ', text).lower()


def word_tokenize(text):
    return nltk.word_tokenize(text)


def pos_tagging(tokens, pos_filter={"NN", "JJ"}):
    tagged = nltk.pos_tag(tokens)
    nouns = [w for (w, pos) in tagged if pos[:2] in pos_filter]
    meaningful = [w for (w, pos) in tagged if pos[:2] in "JJ" and "-" in w]
    return nouns + meaningful


def stemming(tokens):
    return [ps.stem(t) for t in tokens]


def filtering(tokens, filter_terms):
    return [t for t in tokens if t not in filter_terms]


def filtering(tokens, filter_terms):
    return [t for t in tokens if t not in filter_terms]

