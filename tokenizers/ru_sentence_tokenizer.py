#
# Created by maks5507 (me@maksimeremeev.com)
#

import rusenttokenize

class RuSentenceTokenizer:    
    def tokenize(self, text):
        return rusenttokenize.ru_sent_tokenize(text)
