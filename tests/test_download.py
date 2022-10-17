import pytest
import requests
import requests_mock
import os
import tempfile
from page_loader import download



TEST_URL = 'http://test.com'
TEST_FILE_NAME = 'test-com.html'


def test_download():
    dir_path = tempfile.TemporaryDirectory().name
    os.mkdir(dir_path)
    f_name = os.path.join(dir_path, TEST_FILE_NAME)
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='resp')
        assert download('http://test.com', dir_path) == f_name
    with open(f_name) as f:
        assert 'resp' == f.read()