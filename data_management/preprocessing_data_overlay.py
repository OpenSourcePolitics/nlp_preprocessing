"""
This file is used to define an Interface that
will act as an overlay between the script and the input data
"""
import os
import json
import pandas as pd
from dataclasses import dataclass


class NlpPreprocessingDataLoader:
    """
    Interface for data loading
    """

    def load(self):
        """
        method used to load data before it is passed to the processing
        functions
        """
        pass


@dataclass
class InputCorpus:
    filename: str
    data: pd.DataFrame


class LocalPreprocessingDataLoader(NlpPreprocessingDataLoader):
    """
    Implements the main interface and the methods load for
    when a local file is to be preprocessed
    """

    def __init__(self, file_path):
        self._file_path = file_path
        self._filename = os.path.basename(os.path.normpath(os.path.splitext(file_path)[0]))

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
    
    def load_json(self) -> InputCorpus:
        with open(self._file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return InputCorpus(filename=self._filename, data=pd.read_json(data))

    def load_csv(self) -> InputCorpus:
        return InputCorpus(filename=self._filename, data=pd.read_csv(self._file_path, sep=",", encoding="utf-8"))

    def load_xls(self) -> InputCorpus:
        return InputCorpus(filename=self._filename, data=pd.read_excel(self._file_path))


class ApiPreprocessingDataLoader(NlpPreprocessingDataLoader):
    """
    Implements the main interface WordFrequencyLoader to deal
    with the data that send by a post request to the API
    """

    def __init__(self, post_request_data, filename):
        self._post_request_data = post_request_data
        self._filename = filename

    def load(self):
        """
        implements the load method from NlpPreprocessingDataLoader interface
        in case of a post request send by the API and returns both the preprocessed
        word frequencies and the classical one
        """
        post_request_data = pd.DataFrame.from_dict(self._post_request_data, orient='index')
        return InputCorpus(filename=self._filename,
                           data=post_request_data)
