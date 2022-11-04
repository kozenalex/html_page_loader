import pytest
import os, stat
import requests
import requests_mock
import tempfile
from page_loader import download


TEST_URL = 'http://test.com/subdom/'


def test_file_exception():
    with requests_mock.Mocker() as m:
        m.get(TEST_URL, text='foo bar')
        with tempfile.TemporaryDirectory() as dir_name:
            os.chmod(dir_name, stat.S_IRUSR)
            with pytest.raises(PermissionError):
                download(TEST_URL, dir_name)


def test_connection_exception():
    with pytest.raises(requests.ConnectionError):
        download('https://test.test/subdom')


def test_file_exist_exception():
    with requests_mock.Mocker() as m:
        m.get(TEST_URL, text='foo bar')
        with tempfile.TemporaryDirectory() as dir_name:
            with pytest.raises(FileNotFoundError):
                download(TEST_URL, os.path.join(dir_name,'/foo'))
