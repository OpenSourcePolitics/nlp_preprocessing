"""
Project API
"""
import os
import sys
import json
import traceback
from functools import wraps
from flask import Flask, jsonify, request, send_file, make_response
from data_management.utils import clean_dist_directory
from data_management.preprocessing_data_overlay import ApiPreprocessingDataLoader
from main import get_nlp_preprocessing_from_api

API_PATH = os.path.split(os.path.realpath(__file__))[0]
app = Flask(__name__)


def load_preprocessed_data():
    with open(os.path.join(API_PATH, "dist/nlp_preprocessing_output.json"), 'r', encoding='utf-8') as file:
        preprocessing_data = json.load(file)
    return preprocessing_data


@app.teardown_request
def empty_dist_directory(response):
    """
    Function that will be called after the request
    to clean the dist directory
    :param response:
    :return:
    """
    clean_dist_directory(os.path.join(API_PATH, "dist/*"))
    return response


def check_data(func):
    """
    decorator function used to check that the data is not null or invalid
    :param func: function on which the decorator is called
    :return:
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'Invalid data'}), 403
        return func(*args, **kwargs)
    return wrapped


@app.route('/', methods=["POST"])
@check_data
def execute_preprocessing():
    """
    This function get a json file transmitted by the
    client with a POST request.
    It then returns an archive containing the outputs of the script
    :return: Send the contents of a file to the client. see send_file documentation
    for further information
    """
    filename = request.args['filename']
    data = request.get_json()
    try:
        get_nlp_preprocessing_from_api(post_request_data=data, filename=filename)
    except Exception as execution_error:
        print(type(execution_error))
        print(execution_error.args)
        traceback.print_exc(file=sys.stdout)
        print(execution_error)
        return jsonify(
            {'message': 'Error executing script'}
        ), 403
    response = load_preprocessed_data()
    return jsonify(response)


if __name__ == "__main__":
    app.run()
