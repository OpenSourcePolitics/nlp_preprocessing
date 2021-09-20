"""
Project API
"""
import os
import sys
import json
import traceback
import requests
from dotenv import load_dotenv
from functools import wraps
from flask import Flask, jsonify, request
from data_management.utils import clean_dist_directory
from main import get_nlp_preprocessing_from_api
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


API_PATH = os.path.split(os.path.realpath(__file__))[0]

load_dotenv()

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

app = Flask(__name__)

def required_params_are_present(request_args):
    if len(request_args) < 1:
        return False
    
    if 'token' in request_args and 'preprocessing_id' in request_args:
        if request_args["token"] == "" or request_args["preprocessing_id"] == "":
            return False
        else:
            return True
    else:
        return False

def load_preprocessed_data() -> dict:
    with open(os.path.join(API_PATH, "dist/nlp_preprocessing_output.json"), 'r', encoding='utf-8') as file:
        preprocessing_data = json.load(file)
    return preprocessing_data

@app.teardown_request
def once_request_finished(response):
    """
    Function that will be called after the request
    to clean the dist directory
    Furthermore, it makes HTTP POST request to the interface endpoint
    :param token: Request token given as query string
    :param id: Request id given as query string
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
            return jsonify({'message': 'Invalid data'}), 400
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
    try:
        if required_params_are_present(request.args):
            params = {
                "token": request.args['token'],
                "preprocessing_id": request.args['preprocessing_id']
            }
        else:
            return jsonify({'message': 'Required params are missing or invalid'}), 400

        get_nlp_preprocessing_from_api(post_request_data=request.get_json())

        preprocessed_data = load_preprocessed_data()
        requests.post(os.environ.get('RAILS_APP_ENDPOINT'), params=params, json=json.dumps(preprocessed_data))

        return jsonify(preprocessed_data)

    except Exception as execution_error:
        print(type(execution_error))
        print(execution_error.args)
        traceback.print_exc(file=sys.stdout)
        print(execution_error)
        return jsonify(
            {'message': 'An internal server error occured'}
        ), 500


if __name__ == "__main__":
    app.run()
