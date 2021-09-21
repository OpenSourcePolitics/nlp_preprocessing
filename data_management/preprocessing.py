"""
This file stores the functions responsible of textual data preprocessing
such as stop words removal, lower casing, lemmatization etc..
"""
import os
import re
import json
import pandas
import stanza
import nltk
from data_management.preprocessing_data_overlay import InputCorpus


PREPROCESSING_FILE_PATH = os.path.split(os.path.realpath(__file__))[0]


def get_french_stop_words():
    """
    This function will create a set of stop words based on nltk french resources and
    custom information stored in the file stop_words.txt
    :return: set of words
    :rtype: set
    """
    with open(os.path.join(PREPROCESSING_FILE_PATH + '/..',
                           "stop_words.txt"), "r", encoding="utf-8") as file:
        custom_stop_words = file.readlines()
    clean_words = []
    for word in custom_stop_words:
        clean_words.append(re.sub('\n', '', word))
    stop_words = nltk.corpus.stopwords.words("french")
    return set(stop_words + clean_words + ["re", "ré", "er"])


def f_base(string):
    """
    Basic preprocessing : lowercase, suppression of special characters, remove
    remaining letters, suppression of numbers
    :param string: string to be processed
    :return: processed string - see comments in the source code for more info
    """
    string = re.sub(r'[0-9]+|%|[+*\\/_#$]+', '', string)
    string = re.sub(r'[}{\]\[= ><?.;,!":»«]+', ' ', string)
    string = re.sub(r'[()]+', '', string)
    string = re.sub(r'[\-\'’`]+', ' ', string)
    string = re.sub(r' [a-z] | qu ', ' ', string)
    string = re.sub(r' {2}', " ", string)

    return string.strip()


def f_stopwords(w_list):
    """
    filtering out stop words (downgraded to nltk default stop words for french)
    :param w_list: list of words
    :return: list of words without stop_words
    """
    stop_words = get_french_stop_words()
    return [word for word in w_list if word not in stop_words]


def preprocess_pipe_proposal(raw_text):
    """
    cleaning pipe used to process complete proposals
    :param raw_text: proposal to be processed
    :type raw_text: str
    :return: processed proposal
    :rtype: str
    """
    corpora = f_base(raw_text)
    nlp = stanza.Pipeline(lang='fr', processors='tokenize,lemma')
    doc = nlp(corpora)

    lemmas = list(doc.get('lemma'))
    lemmatized_proposals = " ".join(f_stopwords(lemmas))
    return lemmatized_proposals


def get_clean_proposals(corpus: InputCorpus) -> pandas.DataFrame:
    """
    This function will either call the preprocessing pipe on all the proposals and a
    preprocessed_proposals column in data. It then will be stored in the dist directory.
    If the corpus has already been preprocessed it will load it instead to avoid
    useless computation time.
    :return: updated dataframe with a new column storing the preprocessed data
    """
    # local config for pylint -> unwanted message on line 97 (delete the following
    # line to access it)
    # pylint: disable=unnecessary-lambda
    dataframe = corpus.data
    clean_proposals = dataframe["body"].apply(lambda x: preprocess_pipe_proposal(x))
    dataframe["preprocessed_proposals"] = clean_proposals

    json_object = dataframe.to_json(orient="index")
    parsed_object = json.loads(json_object)
    with open(os.path.join(PREPROCESSING_FILE_PATH, "../dist/preprocessed_data.json"), "w", encoding="utf-8") as file:
        json.dump(parsed_object, file, ensure_ascii=False, indent=4)
    return dataframe
