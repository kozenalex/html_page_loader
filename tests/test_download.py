import pytest
import requests
import requests_mock
import os
import tempfile
from page_loader import download



TEST_URL = 'http://test.com/subdom/'
TEST_FILE_NAME = 'test-com-subdom.html'
TEST_RES_DIR_NAME = 'test-com-subdom_files'


def test_download():
    dir_path = tempfile.TemporaryDirectory().name
    os.mkdir(dir_path)
    f_name = os.path.join(dir_path, TEST_FILE_NAME)
    with requests_mock.Mocker() as m:
        m.get(TEST_URL, text='resp')
        assert download(TEST_URL, dir_path) == f_name
    with open(f_name) as f:
        assert 'resp' == f.read()