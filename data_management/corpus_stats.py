"""
This file will be used to compute statistical indicators on text data
"""
import os
from collections import defaultdict
import nltk
import json
from data_management.preprocessing import get_clean_proposals
from data_management.utils import check_category_exists


def freq_stats_corpora(file_path):
    """
    This function returns the corpus as a dictionary where the keys are the different categories
    and the values are the proposals
    :param file_path: path to the initial data
    :type file_path: str
    :return: {label: tokenized proposals}
    :rtype: dict
    """
    dataframe = get_clean_proposals(file_path)
    dataframe = check_category_exists(dataframe)
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    corpora = defaultdict(list)
    df_dict = dataframe.to_dict()
    proposals_as_dict = dataframe['preprocessed_proposals'].to_dict()
    categories = df_dict["category"]
    cpt = 0
    for _, category in categories.items():
        corpora[category] += tokenizer.tokenize(
            list(proposals_as_dict.values())[cpt].lower()
        )
        cpt += 1
    return corpora


def voc_unique(file_path):
    """
    This function will count the number of different words by category
    :param file_path: path to the csv file to study
    :type file_path: str
    :return: dictionary (freq), dictionary (stats), dictionary (corpus)
    :rtype: tuple
    """
    corpora = freq_stats_corpora(file_path)
    freq = dict()
    fq_total = nltk.Counter()

    for keys, values in corpora.items():
        freq[keys] = nltk.FreqDist(values)
        fq_total += freq[keys]
    with open(os.path.join(os.getcwd(), "dist/word_frequency.json"), "w", encoding="utf-8") as json_file:
        json.dump(fq_total, json_file, ensure_ascii=False)
    return fq_total, corpora


def get_most_common_words(file_path, number_of_words=50):
    """
    This function will return the most common words
    :param file_path: path to the initial data
    :param number_of_words: number of most common words
    :return:
    """
    fq_total, _ = voc_unique(file_path)
    most_commons = list(fq_total.most_common(number_of_words))
    return most_commons
