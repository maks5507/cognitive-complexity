#
# Created by maks5507 (me@maksimeremeev.com)
#

from . import pathmagic
pathmagic.add_to_path(2)

from complexity import complexity_model
from tokenizers import word_tokenizer
from functions import distance_cf

import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', nargs='*', help='path to reference collection')
    parser.add_argument('-j', '--jobs', nargs='*', help='number of parallel jobs')
    parser.add_argument('-n', '--name', nargs='*', help='name of the model')
    parser.add_argument('-s', '--stopwords', nargs='*', help='path to stopwords.txt')
    args = parser.parse_args()

    word_tokenizer = word_tokenizer.WordTokenizer(stopwords=args.stopwords[0])
    lexical_distance_complexity_function = distance_cf.DistanceComplexityFunction()
    model = complexity_model.ComplexityModel(word_tokenizer, lexical_distance_complexity_function)
    model.fit(args.path[0], use_preproc=False, n_jobs=args.jobs[0])

    model.dump(path='.', model_name=args.name[0])
