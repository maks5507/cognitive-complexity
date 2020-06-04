#
# Created by maks5507 (me@maksimeremeev.com)
#

import ufal.udpipe


class Model:
    def __init__(self, path):
        self.model = ufal.udpipe.Model.load(path)

    def tokenize(self, text):
        tokenizer = self.model.newTokenizer(self.model.DEFAULT)
        return self._read(text, tokenizer)

    def read(self, text, in_format):
        input_format = ufal.udpipe.InputFormat.newInputFormat(in_format)
        return self._read(text, input_format)

    def _read(self, text, input_format):
        input_format.setText(text)
        error = ufal.udpipe.ProcessingError()
        sentences = []

        sentence = ufal.udpipe.Sentence()
        while input_format.nextSentence(sentence, error):
            sentences.append(sentence)
            sentence = ufal.udpipe.Sentence()
        return sentences

    def tag(self, sentence):
        self.model.tag(sentence, self.model.DEFAULT)

    def parse(self, sentence):
        self.model.parse(sentence, self.model.DEFAULT)

    def write(self, sentences, out_format):
        output_format = ufal.udpipe.OutputFormat.newOutputFormat(out_format)
        output = ''
        for sentence in sentences:
            output += output_format.writeSentence(sentence)
        output += output_format.finishDocument()
        return output
