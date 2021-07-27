"""
File to be run
"""
import os
import json
import argparse
from data_management.utils import load_data, merge_json_objects, clean_dist_directory
from data_management.preprocessing import get_clean_proposals
from data_management.corpus_stats import voc_unique_by_category

MAIN_PATH = os.path.split(os.path.realpath(__file__))[0]


def init_preprocessed_data_tmp_files(file_path):
    """
    This function will call the main function of preprocessing.py and
    corpus_stats.py in order to initialize the tmp json objects that will
    be required by the other analysis projects
    :param file_path: path to the file storing the data to be preprocessed
    :type file_path: str
    """
    clean_dist_directory(os.path.join(MAIN_PATH + "dist/*"))
    preprocessed_dataframe = get_clean_proposals(file_path)
    initial_data = load_data(file_path)
    voc_unique_by_category(preprocessed_dataframe, preprocessed=True)
    voc_unique_by_category(initial_data, preprocessed=False)


def parse_cli_arguments():
    """
    Adds an argument to the cli execution : file_path
    use python main.py -h to access information about the argument.
    :return: list of arguments accessible for a cli execution
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--file_path",
                        type=str,
                        help="path to the Decidim-like data to be preprocessed :"
                             " supported extensions are .xls and .csv",
                        required=True)
    return parser.parse_args()


def nlp_preprocessing_workflow(file_path):
    """
    Main function that will call the the function responsible of the tmp
    files creation and then call the function responsible of their merge into the
    file that will be exposed with the API. Also checks if the file has already been preprocessed
    and
    :param file_path: path to the file storing the data to be preprocessed
    :type file_path: str
    """
    filename = os.path.basename(os.path.normpath(os.path.splitext(file_path)[0]))
    if os.path.isfile(os.path.join(MAIN_PATH, "dist/nlp_preprocessing_output.json")):
        with open(os.path.join(MAIN_PATH, "dist/nlp_preprocessing_output.json"),
                  "r", encoding="utf-8") as final_file:
            data = json.load(final_file)
        if filename == list(data.keys())[0]:
            print("file already preprocessed")
        else:
            init_preprocessed_data_tmp_files(file_path)
            merge_json_objects(file_path)
    else:
        init_preprocessed_data_tmp_files(file_path)
        merge_json_objects(file_path)


if __name__ == '__main__':
    ARGS = parse_cli_arguments()
    nlp_preprocessing_workflow(ARGS.file_path)
