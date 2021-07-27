"""
This file stores the functions responsible of textual data preprocessing
such as stop words removal, lower casing, lemmatization etc..
"""
import os
import re
import json
import pandas as pd
import stanza
import nltk
from data_management.utils import load_data, check_preprocessed_file_exists

PREPROCESSING_FILE_PATH = os.path.split(os.path.realpath(__file__))[0]


def get_french_stop_words():
    """
    This function will create a set of stop words based on nltk french resources and
    custom information stored in the file stop_words.txt
    :return: set of words
    :rtype: set
    """
    with open(os.path.join(PREPROCESSING_FILE_PATH+'/..',
                           "stop_words.txt"), "r", encoding="utf-8") as file:
        custom_stop_words = file.readlines()
    clean_words = []
    for word in custom_stop_words:
        clean_words.append(re.sub('\n', '', word))
    stop_words = nltk.corpus.stopwords.words("french")
    return set(stop_words+clean_words)


def f_base(string):
    """
    Basic preprocessing : lowercase, suppression of special characters, remove
    remaining letters, suppression of numbers
    :param string: string to be processed
    :return: processed string - see comments in the source code for more info
    """
    string = string.lower()
    string = re.sub(r'[0-9]+|%|[+*\\/_#$]+', '', string)
    string = re.sub(r'[}{\]\[()= ><?.;,!":»«]+', ' ', string)
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


def get_clean_proposals(file_path, proposal_column_name="body"):
    """
    This function will either call the preprocessing pipe on all the proposals and a
    preprocessed_proposals column in data. It then will be stored in the dist directory.
    If the corpus has already been preprocessed it will load it instead to avoid
    useless computation time.
    :param file_path: path to the data to preprocess -> csv or xls data
    :type file_path: str
    :param proposal_column_name: name of the column storing the proposals
    :type proposal_column_name: str
    :return: updated dataframe with a new column storing the preprocessed data
    """
    # local config for pylint -> unwanted message on line 97 (delete the following
    # line to access it)
    # pylint: disable=unnecessary-lambda

    file_exists, preprocessed_file_path, _ = check_preprocessed_file_exists(file_path)
    if file_exists:
        dataframe = pd.read_json(preprocessed_file_path, orient="index")
    else:
        dataframe = load_data(file_path)
        clean_proposals = dataframe[proposal_column_name].apply(lambda x: preprocess_pipe_proposal(x))
        dataframe["preprocessed_proposals"] = clean_proposals

    json_object = dataframe.to_json(orient="index")
    parsed_object = json.loads(json_object)
    with open(os.path.join(PREPROCESSING_FILE_PATH, "../dist/preprocessed_data.json"), "w", encoding="utf-8") as file:
        json.dump(parsed_object, file, ensure_ascii=False, indent=4)
    return dataframe


def init_txt_file_from_table(file_path, proposal_column_name="body"):
    """
    Write a text file containing only the preprocessed proposals.
    It is created from the dataframe structure initialized by the function
    get_clean_proposals().
    :param file_path: path to the data to preprocess -> csv or xls data
    :type file_path: str
    :param proposal_column_name: name of the column storing the proposals
    :type proposal_column_name: str
    """
    file_exists, preprocessed_file_path, filename = check_preprocessed_file_exists(file_path)
    if file_exists:
        dataframe = pd.read_json(preprocessed_file_path, orient="index")
    else:
        dataframe = get_clean_proposals(file_path, proposal_column_name)
    body = dataframe["preprocessed_proposals"].to_list()
    with open(os.path.join(PREPROCESSING_FILE_PATH, "../dist/{}_preprocessed.txt".format(filename)),
              "w", encoding="utf-8") as file:
        for prop in body:
            file.writelines(prop+'\n')
