"""
File to be run
"""
import os
from data_management.corpus_stats import get_most_common_words

if __name__ == '__main__':
    most_commons_words = get_most_common_words(os.path.join(os.getcwd(), "data/subset_raw_data.csv"), number_of_words=100)

