"""
Integration test file
"""
import os

TEST_PATH_INTEGRATION = os.path.split(os.path.realpath(__file__))[0]


def test_main():
    """
    This function will test the main and assert that the execution went well
    """
    result = os.system("python {}/main.py".format(TEST_PATH_INTEGRATION + "/.."))
    assert result == 0


def test_resources_installation():
    """
    This function is responsible to test the proper functioning of
    stanza and nltk download functionalities
    """
    result = os.system("python {}/resources_installation.py".format(TEST_PATH_INTEGRATION + "/.."))
    assert result == 0
