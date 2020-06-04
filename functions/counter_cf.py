#
# Created by maks5507 (me@maksimeremeev.com)
#

import pickle


class LexicalCounterComplexityFunction():
    def __init__(self, tf_path):
        self.tfs = pickle.load(open(tf_path, 'rb'))
    
    def score(self, token):
        return -self.tfs[token]

    def complexity(self, tokens):
        return [self.score(token) for token in tokens]
