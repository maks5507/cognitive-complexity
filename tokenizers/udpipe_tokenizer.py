#
# Created by maks5507 (me@maksimeremeev.com)
#

from .udpipe_wrapper import Model
from .udpipe_wrapper import Node


class UdPipeTokenizer:
    def __init__(self, model_path):
        self.model = Model(model_path)

    @staticmethod
    def parse_output(out):
        sentences = [[]]
        for line in out.split('\n'):
            if len(line) == 0:
                sentences += [[]]
                continue
            if line[0] == '#':
                continue
            parsed = line.split()
            sentences[-1].append(Node(parsed[1],
                                      parsed[2],
                                      parsed[3],
                                      parsed[4],
                                      parsed[5],
                                      parsed[7],
                                      int(parsed[6]) - 1))
        return sentences

    def tokenize(self, text, use_preproc=False, use_stem=False, use_lemm=False, check_length=False,
                 check_stopwords=False):
        sentences = self.model.tokenize(text)
        for s in sentences:
            self.model.tag(s)
            self.model.parse(s)
        conllu = self.model.write(sentences, "conllu")
        result = self.parse_output(conllu)
        return result
