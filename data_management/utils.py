"""
Tool function used across the module
"""
import os
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
    :param file_path: path to the data
    :type file_path: str
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
    dataframe, filename = check_file_extension(file_path)
    dataframe = check_category_exists(dataframe)
    return dataframe, filename
