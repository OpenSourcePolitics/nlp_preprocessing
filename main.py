"""
File to be run
"""
import os
from data_management.utils import load_data
from data_management.preprocessing import get_clean_proposals
from data_management.corpus_stats import voc_unique_by_category

MAIN_PATH = os.path.split(os.path.realpath(__file__))[0]

if __name__ == '__main__':
    preprocessed_dataframe, filename_preprocessed = get_clean_proposals(os.path.join(MAIN_PATH,
                                                                                     "data/subset_raw_data.csv"))
    initial_data, initial_data_filename = load_data(os.path.join(MAIN_PATH,
                                                                 "data/subset_raw_data.csv"))
    preprocessed_most_commons_words = voc_unique_by_category(preprocessed_dataframe,
                                                             filename=filename_preprocessed,
                                                             preprocessed=True)
    most_common_words = voc_unique_by_category(initial_data,
                                               initial_data_filename,
                                               preprocessed=False)
