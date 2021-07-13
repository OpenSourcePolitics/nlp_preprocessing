"""
Tool function used across the module
"""
import os
import pandas as pd

UTILS_PATH = os.path.split(os.path.realpath(__file__))[0]


def check_file_extension(file_path):
    """

    :param file_path:
    :return:
    """
    filename, file_extension = os.path.splitext(file_path)
    filename = os.path.basename(os.path.normpath(filename))
    if file_extension == ".xls":
        dataframe = pd.read_excel(file_path)
    elif file_extension == ".csv":
        dataframe = pd.read_csv(file_path, sep=",", encoding="utf-8")
    return dataframe, filename


def check_preprocessed_file_exists(file_path):
    """
    This function aims to save computation time if the data already exist
    :return: boolean if file exist, path to said file and filename
    :rtype: tuple
    """
    filename, _ = os.path.splitext(os.path.split(file_path)[1])
    preprocessed_file_path = os.path.join(UTILS_PATH+'/..', "dist/{}_preprocessed.csv".format(filename))
    file_exists = os.path.isfile(preprocessed_file_path)
    return file_exists, preprocessed_file_path, filename


def check_category_exists(dataframe):
    """
    This function will check if a column "category" exists in the initial dataframe.
    If the data is not categorized then it will create a false category for statistical computation purposes
    :return: dataframe updated if it did not have a column category
    """
    if "category" in dataframe.columns:
        pass
    else:
        dataframe["category"] = "false_category"
    return dataframe
