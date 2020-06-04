# Cognitive Complexity Estimation Framework

**Author**: Maksim Eremeev (me@maksimeremeev.com)

**Research**: Konstantin Vorontsov, Maksim Eremeev

Papers:

[RANLP paper](http://maksimeremeev.com/files/eremeev19complexity.pdf),

[Overview in Russian](maksimeremeev/files/voron19complexity.pdf)

This is a framework for testing and experimenting with complexity measures, building and saving models fitted on various reference collections.
The library provides efficient parallel processing of reference collections.

## Requirements

1. python >= 3.6
2. numpy
3. nltk
4. pymorphy2
5. multiprocessing

## Installation

The framework supports

```
python setup.py build
python setup.py install
```

## Progress

1. Implement the basic ```ComplexityModel``` class
2. Parallelization of ```fit``` method
3. Letter, Syllable, and Word Tokenizers for Russian
   - tokenizers:
      - ```letter_tokenizer```, ```word_tokenizer```, ```ru_syllab_tokenizer```
4. Distance-based ComplexityFunction
   - functions:
     - ```distance_cf```
5. Morphological and Lexical complexity models
   - models:
     - ```letters```, ```lexical-distance```,  ```ru-syllab-sorted```, ```ru-syllab```
6. Counter-based ComplexityFunction
   - functions:
     - ```counter_cf```, ```length_cf```
7. Counter-based models
   - models:
     - ```lexial-length```, ```lexical-counter```
8. Adaptation of morphological models for English
   - tokenizers:
     - ```en_syllab_tokenizer```, ```en_syllab_sorted_tokenizer```
   - models:
     - ```en-syllab```, ```en-syllab-sorted```
9. Syntax models based on UdPipe
   - tokenizers:
     - ```udpipe_wrapper```, ```udpipe_tokenizer```, ```udpipe_tokenizer_pos```, ```en_sentence_tokenizer```, ```ru_sentence_tokenizer```
   - functions:
     - ```syntax_length_cf```
   - models:
     - ```syntax-length```, ```syntax-pos```
10. Making preprocessing more flexible
    - tokenizers:
      - ```preprocessor```
11. ```setup.py``` and testing on Ubuntu, OSX
12. Publishing the Open-Source framework

==== You are here ====

13. Publishing the ```ComplexityPipeline``` implementation to fit the aggregated complexity model
14. Publishing of distributions for all proposed models and validation data
15. Enhancement of model weights
... (TBD)

## Structure

1. ```complexity``` - main must-import module
2. ```tokenizers``` - most common tokenizers implementation
3. ```functions``` - most common complexity functions implementation
4. ```data``` - all data used for experimenting

## Reference Collection Format

```ComplexityModel``` uses reference collection to build empirical distributions. The reference collection has to be provided in strictly fixed format.

1. Each document of the collection must be saved in the separate ```.txt``` file. The name of file does not matter.
2. All files containing documents of the reference collection must be stored in the single directory.
3. There should not be empty ```.txt``` files

## Adjusting the model

Complexity model is a combination of two entities - *Tokenizer* and *ComplexityFunction*.

Both *Tokenizer* and *ComplexityFunction* are to be passed into constructor of the model.

*Tokenizer* is instance of some class required to have ```tokenize``` method.

```tokenize(text)``` takes the only argument - ```text```, which is a string corresponding to a single document. Returns the list of tokens in order they are situated in give text. If text should be preprocessed in some way, preprocessing steps have to be implemented in ```tokenize``` method.

Example:

```python
class Tokenizer:
    def tokenize(self, text):
        return text.split()
```

*ComplexityFunction* is instance of the abstract class with the only required method - ```complexity```.

```complexity(tokens)``` takes the output of the ```tokenize``` method, i.e. list of tokens as they are steered in the prior text. Method returns list of complexity scores for each token in the same order.

```python
class ComplexityFunction:
    def complexity(self, tokens):
	return [len(token) for token in tokens]
```

## Signatures and arguments

**Init**

```ComplexityModel``` init options:

1. ```tokenizer``` - Tokenizer instance
2. ```complexity_function``` - ComplexityFunction instance
3. ```alphabet``` - ```'full'``` if alphabet consists of more than one token, ```'reduced'``` otherwise. Default: ```'full'```

Returns: model instance

Example:

```python
tokenizer = Tokenizer()
complexity_function = ComplexityFunction()
cm = ComplexityModel(tokenizer, complexity_function, alphabet='reduced')
```

**Fit**

```fit(reference_corpus, n_jobs=4, use_preproc=True, use_stem=True, use_lemm=False, check_length=True, check_stopwords=True)```

1. reference_corpus - path to directory with documents of reference collection. Each document must be presented in a separated ```*.txt``` file.
2. n_jobs - number of processes to process the collection. Default: 4
3. use_preproc - flag indicating whether to preprocess the reference collection documents before tokenizing. Default: True
4. use_stem - flag indicating whether to use stemming when preprocessing the reference collection documents. Default: True
5. use_lemm - flag indicating whether to use lemmatization when preprocessing the reference collection documents. Default: True
6. check_length - flag indicating whether to filter all words shorter than 3 symbols when preprocessing the reference collection documents. Default: True
7. check_stopwords - flag indicating whether to filter stopwords when preprocessing the reference collection documents. Default: True

Returns nothing

```fit``` uses ```multiprocessing``` to process documents of the reference collection in parallel.

Example:

```python
cm.fit('/wikipedia', n_jobs=10, use_preproc=False, use_stem=False, use_lemm=False, check_stopwords=False, check_stopwords=False)
```

**Predict**

```predict(texts, gamma=0.95, weights='mean', p=1, use_preproc=True, use_stem=True, use_lemm=False,
           check_length=True, check_stopwords=True, exp_weights=False,
           weights_min_shift=False, normalize=False, return_token_complexities=False)```

1. ```texts``` - lexts to estimate complexity scores for
2. ```gamma``` - quantile indicator. Default: 0.95
3. ```weights``` - Type of weights to use when counting the scoree. One of following options: ```'mean'```, ```'total'```, ```'excessive'```, ```'excessive_mean'```. Default: ```'mean'```. Default: ```'mean'```
4. ```p``` - power of the weights. Default: 1
5. ```use_preproc``` - lag indicating whether to preprocess text before tokenizing. Must align with the same
            parameter value used for fitting. Default: True
6. ```use_stem``` - flag indicating whether to use lemmatization when preprocessing the text. Must align with the
            same parameter value used for fitting. Default: True
7. ```use_lemm``` - power of the weights. Default: False
8. ```check_length``` - flag indicating whether to filter the words shorter than 3 symbols
            when preprocessing the text. Must align with the same parameter value used for fitting. Default: True
9. ```check_stopwords``` - flag indicating whether to filter the stopwords when preprocessing the text.
            Must align with the same parameter value used for fitting. Default: True
10. ```exp_weights``` - flag indicating whether to apply exponential transformation to weights. Default: False
11. ```weights_min_shift``` - flag indicating whether to subtract the minimum value from the weights. Default: False
12. ```normalize``` - flag indicating whether to normalize the weights. Default: False
13. ```return_token_complexities``` - flag indicating whether to return tokens complexities score along with
            the overall text complexity score. Default: False

Returns list of scores for the texts provided.

## Accessible examples

All following models were described in  

1. ```models/letters``` - distance-based morphological model
   - tokens: letters
   - complexity: distance
2. ```models/lexical-distance``` - distance-based lexical model
   - tokens: words
   - complexity: distance
3. ```models/lexical-counter``` - counter-based lexical model
   - tokens: words
   - complexity: number of occurrences in the reference collection
4. ```models/lexical-length```- counter-based lexical model
   - tokens: words
   - complexity: length of the word
5. ```models/re-syllab``` - distance-based morphological model for Russian
   - tokens: syllables
   - complexity: distance
6. ```models/ru-syllab-sorted``` - distance-based morphological model for Russian
   - tokens: sorted syllables
   - complexity: distance
7. ```models/en-syllab``` - distance-based morphological model for English
   - tokens: syllables
   - complexity: distance
8. ```models/en-syllab-sorted``` - distance-based morphological model for English
   - tokens: sorted syllables
   - complexity: distance
9. ```models/syntax-length``` - counter-based syntactic model
   - tokens: sentences
   - complexity: maximum length of the syntactic dependency
10. ```models/syntax-pos``` - distance-based syntactic model
    - tokens: syntgams
    - complexity: distance


## BibTex

```
@inproceedings{eremeev19ranlp,
	title={Lexical Quantile-Based Text Complexity Measure},
	author={M. A. Eremeev and Konstantin Vorontsov},
	booktitle={RANLP},
	year={2019}
}
```
