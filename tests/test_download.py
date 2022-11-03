import pytest
import requests_mock
import os
import tempfile
from page_loader import download


TEST_URL = 'http://test.com/subdom/'
TEST_FILE_NAME = 'test-com-subdom.html'
TEST_RES_DIR_NAME = 'test-com-subdom_files'
FIXTURE_DIR = './tests/fixtures'
RESOURSES = (
    {'url': 'http://test.com/subdom/123.jpg', 'path': '123.jpg'},
    {'url': 'http://test.com/subdom/234.png', 'path': '234.png'},
    {'url': 'http://test.com/img/456.jpg', 'path': '456.jpg'},
    {'url': 'http://test.com/subdom/script.js', 'path': 'script.js'},
    {'url': 'http://test.com/subdom/style.css', 'path': 'style.css'}
)


@pytest.fixture
def test_html():
    data = {}
    with open(os.path.join(FIXTURE_DIR, 'test.html'), 'rb') as f:
        data['content'] = f.read()
    data['url'] = TEST_URL
    return data


@pytest.fixture
def test_resurses():
    data = []
    for res in RESOURSES:
        test_item = {}
        test_item['url'] = res['url']
        with open(os.path.join(FIXTURE_DIR, res['path']), 'rb') as f:
            test_item['content'] = f.read()
        data.append(test_item)
    return data


def setup_mocks(test_html, test_resurses):
    with requests_mock.Mocker() as m:
        m.get(test_html['url'], content=test_html['content'])
        for r in test_resurses:
            m.get(r['url'], content=r['content'])


def test_download(test_html, test_resurses):
    with tempfile.TemporaryDirectory() as dir_name:
        f_name = os.path.join(dir_name, TEST_FILE_NAME)
        setup_mocks(test_html, test_resurses)
        assert download(TEST_URL, dir_name) == f_name
