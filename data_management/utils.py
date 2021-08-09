"""
Tool function used across the module
"""
import os
import json
import glob
import pandas as pd

UTILS_PATH = os.path.split(os.path.realpath(__file__))[0]


def check_file_extension(file_path):
    """
    This function test the file extension and use
    the adequate method to load the data.
    :param file_path:path to the data
    :type file_path: str
    :return: dataframe, filename
    :rtype: tuple
    """
    _, file_extension = os.path.splitext(file_path)
    if file_extension == ".xls":
        dataframe = pd.read_excel(file_path)
    elif file_extension == ".csv":
        dataframe = pd.read_csv(file_path, sep=",", encoding="utf-8")
    return dataframe


def check_preprocessed_file_exists(file_path):
    """
    This function aims to save computation time if the data already exist
    :param file_path: path to the data
    :type file_path: str
    :return: boolean if file exist, path to said file and filename
    :rtype: tuple
    """
    filename, _ = os.path.splitext(os.path.split(file_path)[1])
    preprocessed_file_path = os.path.join(UTILS_PATH+'/..', "dist/preprocessed_data.json")
    file_exists = os.path.isfile(preprocessed_file_path)
    return file_exists, preprocessed_file_path, filename


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


def load_data(file_path):
    """
    This functions is used to load the data which will be preprocessed. It deals
    with csv and xls and will create a category if there is none
    :param file_path: path to the data
    :return: dataframe, filename
    :rytpe: tuple
    """
    dataframe = check_file_extension(file_path)
    dataframe = check_category_exists(dataframe)
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


def merge_json_objects(file_path):
    """
    This function will be used to merge the temporary json outputs (word frequency, preprocessed
    data etc.) and aggregate them into a single json object.
    :param file_path: path to the initial data to be preprocessed
    :type file_path: str
    """
    filename = os.path.basename(os.path.normpath(os.path.splitext(file_path)[0]))
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
        filename: preprocessed_data,
        "word_frequency_preprocessed": word_frequency_preprocessed,
        "word_frequency": word_frequency_data
    }
    with open(os.path.join(UTILS_PATH, "../dist/nlp_preprocessing_output.json"), "w", encoding="utf-8") as file:
        json.dump(merged_dict, file, ensure_ascii=False, indent=4)
