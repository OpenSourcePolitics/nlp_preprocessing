"""
Integration test file
"""
import os
import pytest

TEST_PATH_INTEGRATION = os.path.split(os.path.realpath(__file__))[0]

TEST_FILES = [os.path.join(os.path.dirname(TEST_PATH_INTEGRATION), "data/subset_raw_data.csv"),
              os.path.join(os.path.dirname(TEST_PATH_INTEGRATION), "data/subset_FEAMP.xls")]


@pytest.mark.parametrize("file_path", TEST_FILES)
def test_main(file_path):
    """
    This function will test the main and assert that the execution went well
    """
    result = os.system("python {} -f {}".format(os.path.join(os.path.dirname(TEST_PATH_INTEGRATION),
                                                             "main.py"), file_path))
    assert result == 0


def test_resources_installation():
    """
    This function is responsible to test the proper functioning of
    stanza and nltk download functionalities
    """
    result = os.system("python {}".format(os.path.join(os.path.dirname(TEST_PATH_INTEGRATION),
                                                       "resources_installation.py")))
    assert result == 0
