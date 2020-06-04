#
# Created by maks5507 (me@maksimeremeev.com)
#

import pymorphy2
import re
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import PorterStemmer


class Preprocessing:
    def __init__(self, stopwords):
        self.rgc = re.compile("[^a-zа-яё0-9-_]")
        self.tokenizer = ToktokTokenizer()
        self.lemmatizer = pymorphy2.MorphAnalyzer()
        self.stemmer = PorterStemmer()

        with open(stopwords, 'r') as f:
            self.stopwords = set(f.read().split('\n'))

    def preproc(self, text, check_stopwords=True, check_length=True, use_lemm=False, use_stem=False):
        s = re.sub("\n", r" ", text)
        s = re.sub("'", r" ", s)
        s = s.lower()
        s = self.rgc.sub(" ", s)

        final_agg = []
        tf = {}

        for i, token in enumerate(self.tokenizer.tokenize(s)):
            if check_length and len(token) < 2:
                continue
            if token[-1] == '-' or token[0] == '-':
                continue
            if use_lemm:
                token = self.lemmatizer.parse(token)[0].normal_form
            if use_stem:
                token = self.stemmer.stem(token)
            if token not in self.stopwords or not check_stopwords:
                if token not in tf:
                    tf[token] = 0
                tf[token] += 1
                final_agg.append(token)

        return ' '.join(final_agg), tf