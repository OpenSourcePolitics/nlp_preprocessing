"""
This file will be used to compute statistical indicators on text data
"""
import os
from collections import defaultdict
import json
import nltk
import pandas
from data_management.utils import check_category_exists

STATS_PATH = os.path.split(os.path.realpath(__file__))[0]


def freq_stats_corpora(dataframe: pandas.DataFrame, is_preprocessed=True) -> dict:
    """
    This function returns the corpus as a dictionary where the keys are the different categories
    and the values are the proposals
    :return: {label: tokenized proposals}
    """
    # local config for pylint -> unwanted message on line 29-30 (delete the following
    # line to access it)
    # pylint: disable=no-member
    # pylint: disable=unsubscriptable-object
    dataframe = check_category_exists(dataframe)
    df_dict = dataframe.to_dict()
    if is_preprocessed:
        proposals_as_dict = dataframe['preprocessed_proposals'].to_dict()
    else:
        proposals_as_dict = dataframe["body"].to_dict()
    tokenizer = nltk.RegexpTokenizer(r'\!|\w+')
    corpora = defaultdict(list)
    categories = df_dict["category"]
    cpt = 0
    for _, category in categories.items():
        corpora[category] += tokenizer.tokenize(
            list(proposals_as_dict.values())[cpt].lower()
        )
        cpt += 1
    return corpora


def voc_unique_by_category(dataframe: pandas.DataFrame, is_preprocessed=True):
    """
    This function will count the number of different words by category
    output format -> dictionary (freq), dictionary (stats), dictionary (corpus)
    """
    corpora = freq_stats_corpora(dataframe, is_preprocessed)
    word_frequency_by_category = dict()
    for keys, values in corpora.items():
        word_frequency_by_category[keys] = dict(nltk.FreqDist(values))
    if is_preprocessed:
        with open(os.path.join(STATS_PATH+'/..', "dist/word_frequency_preprocessed.json"),
                  "w", encoding="utf-8") as json_file:
            json.dump(word_frequency_by_category, json_file, ensure_ascii=False)
    else:
        with open(os.path.join(STATS_PATH+'/..', "dist/word_frequency.json"),
                  "w", encoding="utf-8") as json_file:
            json.dump(word_frequency_by_category, json_file, ensure_ascii=False)
