"""
Test preprocessing functionalities
"""
import os
import glob
import pytest

from data_management.preprocessing import get_french_stop_words, f_stopwords, f_base, \
    get_clean_proposals, init_txt_file_from_table, preprocess_pipe_proposal

from data_management.utils import check_preprocessed_file_exists

TEST_PATH_PREPROCESSING = os.path.split(os.path.realpath(__file__))[0]
VAR_1 = [(os.path.join(TEST_PATH_PREPROCESSING + "/..", "data/subset_FEAMP.xls"), "clean_directory"),
         (os.path.join(TEST_PATH_PREPROCESSING + "/..", "data/subset_FEAMP.xls"), None),
         (os.path.join(TEST_PATH_PREPROCESSING + "/..", "data/subset_raw_data.csv"), "clean_directory"),
         (os.path.join(TEST_PATH_PREPROCESSING + "/..", "data/subset_raw_data.csv"), None)]


def clean_dist_directory():
    """
    This function will clean the ./dist directory by deleting all
    files in order to test the different scenarios in the
    preprocessing functions
    """
    former_files = glob.glob(TEST_PATH_PREPROCESSING + '/../dist/*')
    for file in former_files:
        os.remove(file)


def check_is_letters(sentence):
    """
    This function is used to check if a string contains only letters.
    it works by splitting the string in words and check for each word if there are
    not any special characters.
    :param sentence: initial string to be tested
    :type sentence: str
    :return: true if all words are only strings, false otherwise
    :rtype: bool
    """
    only_letters = []
    for word in sentence.split():
        only_letters.append(word.isalpha())
    return all(only_letters)


def check_word_removal(list_of_words):
    """
    This function is used to check that stop word removal worked
    correctly and that there are no remaining words which should have been removed in the
    list returned by f_stopwords.
    :param list_of_words: list of words returned by f_stopwords
    :type list_of_words: list
    :return: true if there are no words in the list that are present in the list of stopwords.
    return false otherwise
    :rtype: bool
    """
    validation = []
    stop_words = get_french_stop_words()
    for word in list_of_words:
        if word not in stop_words:
            validation.append(True)
        else:
            validation.append(False)
    return all(validation)


def test_stop_words():
    """
    This function is used to test the type of the get_french_stop_words() output
    and to assert that the file stop_words.txt is present
    """
    stopwords = get_french_stop_words()
    assert isinstance(stopwords, set) and \
           os.path.isfile(TEST_PATH_PREPROCESSING + "/../stop_words.txt")


def test_stop_word_removal_type():
    """
    Functions used to check f_stopwords rtype and that there are no stop words left
    """
    str_test = "Inciter toutes les entreprises " \
               "à s équiper de panneaux solaires, afin d utiliser toute la surface disponible" \
               " et tendre vers tjrs plus d autonomie énergétique," \
               " au lieu d en installer dans des champs qui pourraient servir pour l agriculture."
    words_list = str_test.split()
    interesting_words = f_stopwords(words_list)
    assert isinstance(interesting_words, list) and check_word_removal(interesting_words)


def test_basic_cleaning():
    """
    This function is used to check f_base return type and to check that there are no
    remaining characters other than letters in the words.
    """
    str_test = r"Inciter toutes + [' {les$ entreprises " \
               r"à s équiper de panneaux \ - > ` solaires, afin d utiliser toute la surface disponible" \
               r" et tendre vers tjrs / plus d autonomie énergétique," \
               r" au lieu d en installer< > dans des champs qui pourraient servir pour l agriculture. ."
    clean_str = f_base(str_test)
    assert isinstance(clean_str, str) and check_is_letters(clean_str)


@pytest.mark.parametrize("file_path, flag_clean_directory", VAR_1)
def test_preprocessing(file_path, flag_clean_directory):
    """
    This function will check that the column preprocessed_proposals is created
    in the dataframe in order to make sure that the rest of the functions will be able to
    operate. It will also check that the list is not empty
    :param file_path: path to the test data -> test for .xls and .csv configurations
    """
    if flag_clean_directory is not None:
        clean_dist_directory()
    dataframe, filename = get_clean_proposals(file_path)
    preprocessed_sentences = dataframe["preprocessed_proposals"].to_list()
    assert "preprocessed_proposals" in list(dataframe.columns) \
           and len(preprocessed_sentences) != 0 \
           and isinstance(filename, str)


@pytest.mark.parametrize("file_path, flag_clean_directory", VAR_1)
def test_txt_creation(file_path, flag_clean_directory):
    """
    This function is used to assert that there is a .txt file created by the function
    init_txt_file_from_table
    :param file_path: path to the test data -> test for .xls and .csv configurations
    """
    if flag_clean_directory is not None:
        clean_dist_directory()
    init_txt_file_from_table(file_path)
    _, _, filename = check_preprocessed_file_exists(file_path)
    assert os.path.isfile(TEST_PATH_PREPROCESSING + "/../dist/{}_preprocessed.txt".format(filename))


def test_preprocessing_pipe():
    """
    This function is used to check the type of the the preprocessing pipe's output
    """
    str_test = r"Inciter toutes + [' {les entreprises " \
               r"à s équiper de panneaux \ - > ` solaires, afin d utiliser toute la surface disponible" \
               r" et tendre vers tjrs / plus d autonomie énergétique," \
               r" au lieu d en installer< > dans des champs qui pourraient servir pour l agriculture. ."
    preprocessed_str = preprocess_pipe_proposal(str_test)
    assert isinstance(preprocessed_str, str)
