"""
Tool function used across the module
"""
import os
import json
import glob

from data_management.preprocessing_data_overlay import InputCorpus

UTILS_PATH = os.path.split(os.path.realpath(__file__))[0]


def clean_keys(data):
    """
    This function will clean the keys of the post request data
    :param data: dictionary containing the data from the post request
    :return: dictionary containing the cleaned data from the post request
    """
    new_dict = {}
    for key, value in data.items():
        new_key = key.replace("/fr", "")
        new_dict[new_key] = clean_keys(value) if isinstance(value, dict) else value
    return new_dict


def check_category_exists(dataframe):
    """
    This function will check if a column "category" exists in the initial dataframe.
    If the data is not categorized then it will create a false category for statistical computation purposes
    :param dataframe: pandas dataframe object storing the data
    :return: dataframe updated if it did not have a column category
    """
    if "category" in dataframe.columns:
        pass
    else:
        dataframe["category"] = "false_category"
    return dataframe


def clean_dist_directory(repository_path):
    """
    This function will clean the ./dist directory by deleting all
    files in order to test the different scenarios in the
    preprocessing functions
    """
    former_files = glob.glob(repository_path)
    for file in former_files:
        os.remove(file)


def merge_json_objects(corpus: InputCorpus):
    """
    This function will be used to merge the temporary json outputs (word frequency, preprocessed
    data etc.) and aggregate them into a single json object.
    """
    with open(os.path.join(UTILS_PATH, "../dist/preprocessed_data.json"),
              "r", encoding="utf-8") as preprocessed_data_file:
        preprocessed_data = json.load(preprocessed_data_file)
    with open(os.path.join(UTILS_PATH, "../dist/word_frequency.json"),
              "r", encoding="utf-8") as word_frequency_file:
        word_frequency_data = json.load(word_frequency_file)
    with open(os.path.join(UTILS_PATH, "../dist/word_frequency_preprocessed.json"),
              "r", encoding="utf-8") as wf_preprocessed_file:
        word_frequency_preprocessed = json.load(wf_preprocessed_file)
    merged_dict = {
        "preprocessed_data": preprocessed_data,
        "word_frequency_preprocessed": word_frequency_preprocessed,
        "word_frequency": word_frequency_data
    }
    with open(os.path.join(UTILS_PATH, "../dist/nlp_preprocessing_output.json"), "w", encoding="utf-8") as file:
        json.dump(merged_dict, file, ensure_ascii=False, indent=4)
