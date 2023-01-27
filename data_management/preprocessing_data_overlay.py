"""
This file is used to define an Interface that
will act as an overlay between the script and the input data
"""
import json
from dataclasses import dataclass
import pandas as pd


class NlpPreprocessingDataLoader:
    """
    Interface for data loading
    """

    def load(self):
        """
        method used to load data before it is passed to the processing
        functions
        """


@dataclass
class InputCorpus:
    """
    Data structure used to store both the name of the corpus
    and the data as a dataframe
    """
    data: pd.DataFrame


class LocalPreprocessingDataLoader(NlpPreprocessingDataLoader):
    """
    Implements the main interface and the methods load for
    when a local file is to be preprocessed
    """

    def __init__(self, file_path):
        self._file_path = file_path

    def load(self) -> InputCorpus:
        """
        implements the load method from WordFrequencyLoader interface
        in case of a local execution. It will load the data stored in a json file.
        and return both the preprocessed
        word frequencies and the classical one
        """
        extension = self._file_path.split('.')[1]
        if extension == 'json':
            return self.load_json()
        elif extension == "csv":
            return self.load_csv()
        elif extension == "xls":
            return self.load_xls()
        else:
            raise ValueError("File extension not supported")

    def load_json(self) -> InputCorpus:
        """
        loads the data from a json file
        """
        with open(self._file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return InputCorpus(data=pd.DataFrame.from_dict(data, orient='index'))

    def load_csv(self) -> InputCorpus:
        """
        loads the data from a csv file
        """
        return InputCorpus(data=pd.read_csv(self._file_path, sep=",", encoding="utf-8"))

    def load_xls(self) -> InputCorpus:
        """
        loads the data from a xls file
        """
        return InputCorpus(data=pd.read_excel(self._file_path))


class ApiPreprocessingDataLoader(NlpPreprocessingDataLoader):
    """
    Implements the main interface WordFrequencyLoader to deal
    with the data that send by a post request to the API
    """

    def __init__(self, post_request_data):
        self._post_request_data = post_request_data

    def load(self):
        """
        implements the load method from NlpPreprocessingDataLoader interface
        in case of a post request send by the API and returns both the preprocessed
        word frequencies and the classical one
        """
        post_request_data = pd.DataFrame.from_dict(self._post_request_data, orient='index')
        return InputCorpus(data=post_request_data)
