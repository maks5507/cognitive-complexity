#
# Created by maks5507 (me@maksimeremeev.com)
#

from . import pathmagic
pathmagic.add_to_path(2)

from complexity import complexity_model
from tokenizers import word_tokenizer
from functions import length_cf

import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', nargs='*', help='path to reference collection')
    parser.add_argument('-j', '--jobs', nargs='*', help='number of parallel jobs')
    parser.add_argument('-n', '--name', nargs='*', help='name of the model')
    parser.add_argument('-s', '--stopwords', nargs='*', help='path to stopwords.txt')
    args = parser.parse_args()

    word_lemmatized_tokenizer = word_tokenizer.WordTokenizer(stopwords=args.stopwords[0])
    lexical_length_complexity_function = length_cf.LengthComplexityFunction()
    model = complexity_model.ComplexityModel(word_lemmatized_tokenizer,
                                             lexical_length_complexity_function, alphabet='reduced')
    model.fit(args.path[0], use_preproc=False, n_jobs=args.jobs[0])

    model.dump(path='.', model_name=args.name[0])
