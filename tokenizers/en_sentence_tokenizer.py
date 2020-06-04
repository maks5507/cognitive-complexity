#
# Created by maks5507 (me@maksimeremeev.com)
#

from nltk.tokenize import sent_tokenize
import spacy


class EnSentenceTokenizer:
    def __init__(self, mode='classic'):
        self.mode = mode
        self.spacy_model = spacy.load('en_core_web_lg')
    
    def tokenize(self, text):
        if self.mode == 'classic':
            return sent_tokenize(text)
        spacy_text = self.spacy_model(text)
        return [sentence for sentence in spacy_text.sents]
