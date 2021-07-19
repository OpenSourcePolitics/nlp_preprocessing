"""
Test statistical functions
"""
import os
import collections
import pytest
from data_management.preprocessing import get_clean_proposals
from data_management.corpus_stats import freq_stats_corpora, voc_unique_by_category
from data_management.utils import load_data

TEST_PATH_STATISTICS = os.path.split(os.path.realpath(__file__))[0]
VAR_1 = [(os.path.join(TEST_PATH_STATISTICS + "/..", "data/subset_FEAMP.xls"), True),
         (os.path.join(TEST_PATH_STATISTICS + "/..", "data/subset_FEAMP.xls"), False),
         (os.path.join(TEST_PATH_STATISTICS + "/..", "data/subset_raw_data.csv"), True),
         (os.path.join(TEST_PATH_STATISTICS + "/..", "data/subset_raw_data.csv"), False)]


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
        dataframe, _ = get_clean_proposals(file_path)
    else:
        dataframe, _ = load_data(file_path)
    categories_df = list(dataframe.category.unique())
    corpora = freq_stats_corpora(dataframe, preprocessed)
    assert isinstance(corpora, collections.defaultdict)\
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
        dataframe, filename = get_clean_proposals(file_path)
    else:
        dataframe, filename = load_data(file_path)
    word_frequency = voc_unique_by_category(dataframe, filename, preprocessed)
    assert len(word_frequency.keys()) == len(set(word_frequency.keys()))\
           and isinstance(word_frequency, dict)
