#
# Created by maks5507 (me@maksimeremeev.com)
#

import numpy as np
import multiprocessing
import pickle
import traceback
from pathlib import Path
import os

from . import utils


class ComplexityModel:
    """
    :Description: Complexity Model class, used to fit and estimate cognitive complexity scores
    :param tokenizer: instance of Tokenizer class to split the texts into tokens
    :type tokenizer: Tokenizer
    :param complexity_function: instance of ComplexityFunction class to estimate a
     complexity score for the single token
    :type complexity_function: ComplexityFunction
    :param alphabet: ``full`` if the distributions are counted for each token (distance-based models),
     ``reduced`` if there only distribution is counted over all tokens (counter-based models), defaults to ``full``.
    :type alphabet: str, optional
    """
    def __init__(self, tokenizer, complexity_function, alphabet='full'):
        self.tokenizer = tokenizer
        self.complexity_function = complexity_function
        self.alphabet = alphabet
        self.distributions = {}
        self.quantiles = {}
        self.min_value = np.nan
        self.min_values = {}
        self.quantile = 0
        self.gamma = -1

    @staticmethod
    def __build_distribution(reference_corpus, queue, tokenizer, complexity_function,
                            alphabet, use_preproc, use_stem, use_lemm, check_length, check_stopwords):
        distributions = {}
        for file in reference_corpus:
            try:
                with open(file, 'r') as f:
                    text = f.read()
                tokens = tokenizer.tokenize(text, use_preproc=use_preproc, use_stem=use_stem,
                                            use_lemm=use_lemm, check_length=check_length,
                                            check_stopwords=check_stopwords)
                complexities = complexity_function.complexity(tokens)
                if alphabet == 'full':
                    for token, score in zip(tokens, complexities):
                        if token not in distributions:
                            distributions[token] = {}
                        if score not in distributions[token]:
                            distributions[token][score] = 0
                        distributions[token][score] += 1
                elif alphabet == 'reduced':
                    for score in complexities:
                        if score not in distributions:
                            distributions[score] = 0
                        distributions[score] += 1
            except KeyboardInterrupt:
                break
            except:
                print(traceback.format_exc())
                continue
        queue.put(distributions)

    def __union_distributions(self, chunks_distributions):
        distributions = {}
        for chunk_distribution in chunks_distributions:
            if self.alphabet == 'full':
                for token in chunk_distribution:
                    if token not in distributions:
                        distributions[token] = chunk_distribution[token]
                        continue
                    for score in chunk_distribution[token]:
                        if score not in distributions[token]:
                            distributions[token][score] = 0
                        distributions[token][score] += chunk_distribution[token][score]
            elif self.alphabet == 'reduced':
                for score in chunk_distribution:
                    if score not in distributions:
                        distributions[score] = chunk_distribution[score]
                        continue
                    distributions[score] += chunk_distribution[score]
        return distributions

    @staticmethod
    def __split_collection(reference_corpus_path, n_jobs):
        files = [filename for filename in Path(reference_corpus_path).rglob('*.txt')]
        chunks = np.array_split(list(files), int(n_jobs))
        return chunks

    @staticmethod
    def __count_quantile(distribution, gamma):
        gamma = 1 - gamma
        size = sum(distribution.values())
        current_amount = 0
        prev_score = 1e18
        sorted_distribution = sorted(distribution.items(),
                                     key=lambda item: item[0], reverse=True)
        for score, amount in sorted_distribution:
            if current_amount + amount > size * gamma:
                return prev_score
            prev_score = score
            current_amount += amount
        return sorted_distribution[-1][0]

    def fit(self, reference_corpus, n_jobs=4, use_preproc=True,
                use_stem=True, use_lemm=False, check_length=True, check_stopwords=True):
        """
        :Description: fits the complexity model given the reference collection
        :param reference_corpus: Path to the directory with reference collection. Directory should contain only *.txt
         files with each file containing text of a single document
        :type reference_corpus: str
        :param n_jobs: Number of parallel jobs processing the reference collection, defaults to 4
        :type n_jobs: int, optional
        :param use_preproc: flag indicating whether to preprocess the reference collection documents before tokenizing,
         defaults to True
        :type use_preproc: bool, optional
        :param use_stem: flag indicating whether to use stemming when preprocessing the reference collection documents,
         defaults to True
        :type use_stem: bool, optional
        :param use_lemm: flag indicating whether to use lemmatization when preprocessing the reference collection
         documents, defaults to True
        :type use_lemm: bool, optional
        :param check_length: flag indicating whether to filter all words shorter than 3 symbols when preprocessing
         the reference collection documents, defaults to True
        :type check_length: bool, optional
        :param check_stopwords: flag indicating whether to filter stopwords when preprocessing the reference
         collection documents, defaults to True
        :type check_stopwords: bool, optional
        """
        processes = []
        self.weights_min_values = {}
        self.weights_min_value = np.nan
        try:
            queue = multiprocessing.Queue()
            chunks = self.__split_collection(reference_corpus, n_jobs)
            for chunk in chunks:
                processes += [multiprocessing.Process(target=self.__build_distribution,
                                                      args=[chunk, queue, self.tokenizer,
                                                            self.complexity_function,
                                                            self.alphabet, use_preproc, use_stem,
                                                            use_lemm, check_length, check_stopwords])]
                processes[-1].start()

            chunk_distributions = []
            for i in range(int(n_jobs)):
                chunk_distributions += [queue.get()]

            for process in processes:
                process.terminate()

            self.distributions = self.__union_distributions(chunk_distributions)
        finally:
            for process in processes:
                process.terminate()

    def predict(self, texts, gamma=0.95, weights='mean', p=1, use_preproc=True,
                use_stem=True, use_lemm=False, check_length=True, check_stopwords=True, exp_weights=False,
                weights_min_shift=False, normalize=False, return_token_complexities=False):
        """
        :Description: estimates the complexity scores of the given set of texts
        :param texts: texts to estimate complexity scores for
        :type texts: list[str]
        :param gamma: quantile indicator, defaults to 0.95
        :type gamma: float, optional
        :param weights: types of weights to use when counting the scores, defaults to ``mean``
        :type weights: str, optional
        :param p: power of the weights, defaults to 1
        :type p: int, optional
        :param use_preproc: flag indicating whether to preprocess text before tokenizing. Must align with the same
            parameter value used for fitting, defaults to True
        :type use_preproc: bool, optional
        :param use_stem: flag indicating whether to use stemming when preprocessing the text. Must align with the
            same parameter value used for fitting, defaults to True
        :type use_stem: bool, optional
        :param use_lemm: flag indicating whether to use lemmatization when preprocessing the text. Must align with the
            same parameter value used for fitting, defaults to False
        :type use_lemm: bool, optional
        :param check_length: flag indicating whether to filter the words shorter than 3 symbols
            when preprocessing the text. Must align with the same parameter value used for fitting, defaults to True
        :type check_length: bool, optional
        :param check_stopwords: flag indicating whether to filter the stopwords when preprocessing the text.
            Must align with the same parameter value used for fitting, defaults to True
        :type check_stopwords: bool, optional
        :param exp_weights: flag indicating whether to apply exponential transformation to weights, defaults to False
        :type exp_weights: bool, optional
        :param weights_min_shift: flag indicating whether to subtract the minimum value from the weights,
            defaults to False
        :type weights_min_shift: bool, optional
        :param normalize: flag indicating whether to normalize the weights, defaults to False
        :type normalize: bool, optional
        :param return_token_complexities: flag indicating whether to return tokens complexities score along with
            the overall text complexity score, defaults to False
        :type return_token_complexities: bool, optional
        """
        if gamma != self.gamma:
            if self.alphabet == 'full':
                for token in self.distributions:
                    self.quantiles[token] = self.__count_quantile(self.distributions[token], gamma)
            elif self.alphabet == 'reduced':
                self.quantile = self.__count_quantile(self.distributions, gamma)
            self.gamma = gamma

        if weights_min_shift:
            if self.alphabet == 'full' and np.isnan(self.min_value):
                self.min_value = min([min(self.distributions[token].keys()) for token in self.distributions])
            if self.alphabet == 'reduced' and np.isnan(self.min_value):
                self.min_value = min(self.distributions.keys())

        texts_complexities = []
        token_complexities = []
        for text in texts:
            tokens = self.tokenizer.tokenize(text, use_preproc=use_preproc, use_stem=use_stem,
                                             use_lemm=use_lemm, check_length=check_length,
                                             check_stopwords=check_stopwords)
            nd = len(tokens)
            complexities = self.complexity_function.complexity(tokens)
                                                               
            weight_scores = []
            is_complex = []
            complexity = 0
            total_score = 0
            for token, score in zip(tokens, complexities):
                weight = 0
                if weights == 'count':
                    weight = 1
                if weights == 'mean':
                    weight = score / nd
                    if weights_min_shift:
                        weight = (score + abs(self.min_value) + 1) / nd
                if weights == 'total':
                    weight = score
                    if weights_min_shift:
                        weight = score + abs(self.min_value) + 1

                if self.alphabet == 'full':
                    if token not in self.quantiles:
                        current_quantile = score
                    else:
                        current_quantile = self.quantiles[token]
                    if weights == 'excessive':
                        weight = score - current_quantile
                    if weights == 'excessive_mean':
                        weight = (score - current_quantile) / nd
                    if exp_weights:
                        weight = np.tanh(weight)
                    complexity += weight ** p * (score >= current_quantile)
                    total_score += weight ** p
                    is_complex += [score >= current_quantile]
                elif self.alphabet == 'reduced':
                    if weights == 'excessive':
                        weight = score - self.quantile
                    if weights == 'excessive_mean':
                        weight = (score - self.quantile) / nd
                    complexity += weight ** p * (score >= self.quantile)
                    total_score += weight ** p
                    is_complex += [score >= self.quantile]
                weight_scores += [weight]
            if normalize:
                texts_complexities += [complexity / total_score]
            else:
                texts_complexities += [complexity]
            if return_token_complexities:
                token_complexities += list(zip(complexities, weight_scores, is_complex))
        return texts_complexities, token_complexities

    def dump(self, path='.', model_name='complexity-model'):
        """
        :Description: dumps the fitted complexity model
        :param path: path to save the dump to, defaults to ``.``
        :type path: str, optional
        :param model_name: name of the dump directory, defaults to ``complexity-model``
        :type model_name: str, optional
        """
        fullpath = os.path.join(path, model_name)
        utils.create_folder(fullpath)
        parameters = {'alphabet': self.alphabet, 'gamma': self.gamma,
                      'distributions': self.distributions, 'quantiles': self.quantiles,
                      'quantile': self.quantile}
        parameters_path = os.path.join(fullpath, 'parameters.bin')
        pickle.dump(parameters, open(parameters_path, 'wb'))

    @staticmethod
    def load(path, tokenizer, complexity_function):
        """
        :Description: loads the instance from the dump directory
        :param path: path to the dump
        :type path: str
        :param tokenizer: instance of Tokenizer class, used for fitting the model
        :type tokenizer: Tokenizer
        :param complexity_function: instance of ComplexityFunction class, used for fitting the model
        :type complexity_function: ComplexityFunction
        """
        model = pickle.load(open(path, 'rb'))
        instance = ComplexityModel(tokenizer, complexity_function,
                                   alphabet=model['alphabet'])
        instance.distributions = model['distributions']
        instance.gamma = model['gamma']
        instance.quantile = model['quantile']
        instance.quantiles = model['quantiles']
        return instance
