#
# Created by maks5507 (me@maksimeremeev.com)
#

import rusyllab
from . import preprocessor


class RuSyllabSortedTokenizer():
    def __init__(self, stopwords):
        self.preprocessor = preprocessor.Preprocessing(stopwords)

    def tokenize(self, text, use_preproc=False, use_stem=False, use_lemm=False,
                 check_length=True, check_stopwords=True):

        preprocessed_text = text

        if use_preproc:
            preprocessed_text, _ = self.preprocessor.preproc(text, use_lemm=use_lemm,
                                                             use_stem=use_stem, check_stopwords=check_stopwords,
                                                             check_length=check_length)

        syllables = rusyllab.split_words(preprocessed_text.split())

        for i in range(len(syllables)):
            syllables[i] = ''.join(sorted(syllables[i]))

        return list(filter(lambda syl: syl != ' ', syllables))