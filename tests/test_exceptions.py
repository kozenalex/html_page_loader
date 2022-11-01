import pytest
import requests
from page_loader import download


def test_file_exception():
    with pytest.raises(PermissionError):
        download('https://ya.ru', '/etc')


def test_connection_exception():
    with pytest.raises(requests.ConnectionError):
        download('https://test.test/subdom')


def test_file_exist_exception():
    with pytest.raises(FileNotFoundError):
        download('https://ya.ru', './fixtures')
