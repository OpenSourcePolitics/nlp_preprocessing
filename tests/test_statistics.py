"""
Test statistical functions
"""
import os
import collections
import json
import pytest
from data_management.utils import check_category_exists
from data_management.preprocessing import get_clean_proposals
from data_management.corpus_stats import freq_stats_corpora, voc_unique_by_category
from data_management.preprocessing_data_overlay import LocalPreprocessingDataLoader

TEST_PATH_STATISTICS = os.path.split(os.path.realpath(__file__))[0]
VAR_1 = [(os.path.join(os.path.dirname(TEST_PATH_STATISTICS), "data/subset_FEAMP.xls"), False),
         (os.path.join(os.path.dirname(TEST_PATH_STATISTICS), "data/subset_FEAMP.xls"), True),
         (os.path.join(os.path.dirname(TEST_PATH_STATISTICS), "data/subset_raw_data.csv"), False),
         (os.path.join(os.path.dirname(TEST_PATH_STATISTICS), "data/subset_raw_data.csv"), True)]


@pytest.mark.parametrize("file_path, preprocessed", VAR_1)
def test_corpora(file_path, preprocessed):
    """
    This function is used to validate the behavior of the freq_stats_corpora
    which will return a defaultdict storing for each category all the proposals
    :param file_path: path to the data
    :type file_path: str
    :param preprocessed: boolean that indicates which resource to use
    :type preprocessed: bool
    """
    if preprocessed:
        corpus = LocalPreprocessingDataLoader(os.path.join(os.path.dirname(TEST_PATH_STATISTICS),
                                                           "dist/preprocessed_data.json")).load()
        dataframe = corpus.data
    else:
        corpus = LocalPreprocessingDataLoader(file_path).load()
        dataframe = get_clean_proposals(corpus)
    dataframe_with_categories = check_category_exists(dataframe)
    categories_df = list(dataframe_with_categories.category.unique())
    corpora = freq_stats_corpora(dataframe, preprocessed)
    assert isinstance(corpora, collections.defaultdict) \
           and len(categories_df) == len(list(corpora.keys()))


@pytest.mark.parametrize("file_path, preprocessed", VAR_1)
def test_voc_uniqueness(file_path, preprocessed):
    """
    use to assert that there is only on instance of each word in the final counter and
    that the type is correct
    :param file_path: path to the data
    :type file_path: str
    :param preprocessed: boolean that indicates which resource to use
    :type preprocessed: bool
    """
    if preprocessed:
        corpus = LocalPreprocessingDataLoader(os.path.join(os.path.dirname(TEST_PATH_STATISTICS),
                                                              "dist/preprocessed_data.json")).load()
        dataframe = corpus.data
    else:
        corpus = LocalPreprocessingDataLoader(file_path).load()
        dataframe = get_clean_proposals(corpus)
    voc_unique_by_category(dataframe, preprocessed)
    if preprocessed:
        with open(os.path.join(os.path.dirname(TEST_PATH_STATISTICS),
                               "dist/word_frequency_preprocessed.json"), 'r', encoding='utf-8') as file:
            word_frequency = json.load(file)
    else:
        with open(os.path.join(os.path.dirname(TEST_PATH_STATISTICS),
                               "dist/word_frequency.json"), 'r', encoding='utf-8') as file:
            word_frequency = json.load(file)
    assert len(word_frequency.keys()) == len(set(word_frequency.keys())) \
           and isinstance(word_frequency, dict)
