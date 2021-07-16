"""
File to be run
"""
import os
from data_management.utils import load_data
from data_management.preprocessing import get_clean_proposals
from data_management.corpus_stats import get_most_common_words

MAIN_PATH = os.path.split(os.path.realpath(__file__))[0]

if __name__ == '__main__':
    preprocessed_dataframe, filename_preprocessed = get_clean_proposals(os.path.join(MAIN_PATH,
                                                                                     "data/subset_raw_data.csv"))
    initial_data, initial_data_filename = load_data(os.path.join(MAIN_PATH,
                                                                 "data/subset_raw_data.csv"))
    preprocessed_most_commons_words = get_most_common_words(preprocessed_dataframe,
                                                            filename=filename_preprocessed,
                                                            preprocessed=True,
                                                            number_of_words=100)
    most_common_words = get_most_common_words(initial_data,
                                              initial_data_filename,
                                              preprocessed=False,
                                              number_of_words=100)

