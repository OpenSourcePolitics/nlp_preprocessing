"""
Test the interface used to deal with different input format
"""
import os
import json
from main import get_nlp_preprocessing_from_api

TEST_DATA_INTERFACE_PATH = os.path.split(os.path.realpath(__file__))[0]


def read_local_data() -> dict:
    """
    Function used to simulate the reception of data through the API
    -> data is passed as a dictionary to the test function
    :return: dictionary storing the corpus to work on
    """
    with open(os.path.join(os.path.dirname(TEST_DATA_INTERFACE_PATH),
                           "data/subset_raw_data.json"), 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def test_api_workflow():
    """
    Tests the execution of the whole workflow from data passed as a dict
    API simulation
    """
    data = read_local_data()
    filename = "subset_raw_data"
    get_nlp_preprocessing_from_api(post_request_data=data, filename=filename)
    assert os.path.isfile(os.path.join(os.path.dirname(TEST_DATA_INTERFACE_PATH), "dist/nlp_preprocessing_output.json"))
