import os
import re
import pandas as pd
import stanza
import nltk
from data_management.utils import check_file_extension, check_preprocessed_file_exists


def get_french_stop_words():
    with open(os.path.join(os.getcwd(), "stop_words.txt"), "r", encoding="utf-8") as file:
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
    string = re.sub(r'[0-9]+|%|[\+\*\\\/\_\#\$]+', '', string)
    string = re.sub(r'[\]\[\(\)\=\>\<\?\.\;\,\!\"\:\»\«]+', ' ', string)
    string = re.sub(r'[\-\'\’]+', ' ', string)
    string = re.sub(r' [a-z]{1} | qu ', ' ', string)
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

    lemmas = [lemma for lemma in doc.get("lemma")]
    lemmatized_proposals = " ".join(f_stopwords(lemmas))
    return lemmatized_proposals


def get_clean_proposals(file_path, proposal_column_name="body"):
    _, filename = check_file_extension(file_path)

    file_exists, preprocessed_file_path, filename = check_preprocessed_file_exists(file_path)
    if file_exists:
        print("This file has already been preprocessed")
        dataframe = pd.read_csv(preprocessed_file_path, sep=";", encoding="utf-8")
    else:
        dataframe, filename = check_file_extension(file_path)
        clean_proposals = dataframe[proposal_column_name].apply(lambda x: preprocess_pipe_proposal(x))
        dataframe["preprocessed_proposals"] = clean_proposals
        dataframe.to_csv(os.path.join(os.getcwd(), "dist/{}_preprocessed.csv".format(filename)),
                         sep=";", encoding="utf-8")
    return dataframe


def init_txt_file_from_table(file_path, proposal_column_name="body"):
    file_exists, preprocessed_file_path, filename = check_preprocessed_file_exists(file_path)
    if file_exists:
        dataframe = pd.read_csv(preprocessed_file_path, sep=',', encoding="utf-8")
    else:
        dataframe = get_clean_proposals(file_path, proposal_column_name)
    body = dataframe["preprocessed_proposals"].to_list()
    with open(os.path.join(os.getcwd(), "dist/{}.txt".format(filename)),
              "w", encoding="utf-8") as file:
        for prop in body:
            file.writelines(prop+'\n')
