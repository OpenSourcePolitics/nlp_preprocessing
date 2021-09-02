"""
File to be run
"""
import os
import argparse
from data_management.utils import merge_json_objects, clean_dist_directory
from data_management.preprocessing import get_clean_proposals
from data_management.corpus_stats import voc_unique_by_category
from data_management.preprocessing_data_overlay import LocalPreprocessingDataLoader, \
    ApiPreprocessingDataLoader, InputCorpus

MAIN_PATH = os.path.split(os.path.realpath(__file__))[0]


def init_preprocessed_data_tmp_files(corpus: InputCorpus):
    """
    This function will call the main function of preprocessing.py and
    corpus_stats.py in order to initialize the tmp json objects that will
    be required by the other analysis projects
    """
    clean_dist_directory(os.path.join(MAIN_PATH + "dist/*"))
    preprocessed_dataframe = get_clean_proposals(corpus)
    voc_unique_by_category(preprocessed_dataframe, is_preprocessed=True)
    voc_unique_by_category(corpus.data, is_preprocessed=False)


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


def get_nlp_preprocessing_from_file(file_path: str):
    """
    Main function for local execution from file. It will initialize the
    preprocessing functions and merge all the data into a single file
    called nlp_preprocessing_output.json
    """
    corpus = LocalPreprocessingDataLoader(file_path).load()
    init_preprocessed_data_tmp_files(corpus)
    merge_json_objects(corpus)


def get_nlp_preprocessing_from_api(post_request_data):
    corpus = ApiPreprocessingDataLoader(post_request_data=post_request_data).load()
    init_preprocessed_data_tmp_files(corpus)
    merge_json_objects(corpus)


if __name__ == '__main__':
    ARGS = parse_cli_arguments()
    get_nlp_preprocessing_from_file(ARGS.file_path)
