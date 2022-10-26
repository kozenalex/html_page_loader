import pytest
import requests
import requests_mock
import os
import tempfile
from page_loader import download



TEST_URL = 'http://test.com/subdom/'
TEST_FILE_NAME = 'test-com-subdom.html'
TEST_RES_DIR_NAME = 'test-com-subdom_files'
FIXTURE_DIR = './tests/fixtures'
IMGS = (
    {'url': 'http://test.com/subdom/123.jpg', 'path': '123.jpg'},
    {'url': 'http://test.com/subdom/234.png', 'path': '234.png'},
    {'url': 'http://test.com/subdom/456.jpg', 'path': '456.jpg'}
)


def test_download():
    dir_path = tempfile.TemporaryDirectory().name
    os.mkdir(dir_path)
    f_name = os.path.join(dir_path, TEST_FILE_NAME)
    expected_files = []
    for i in IMGS:
        expected_files.append(os.path.join(FIXTURE_DIR, i['path']))
    with open(os.path.join(FIXTURE_DIR,'test.html')) as f:
        resp_text = f.read()
    with requests_mock.Mocker() as m:
        m.get(TEST_URL, text=resp_text)
        for i in IMGS:
            with open(os.path.join(FIXTURE_DIR, i['path']), 'rb') as f:
                r_content = f.read()
            m.get(i['url'], content=r_content)
        assert download(TEST_URL, dir_path) == f_name
    assert len(IMGS) == len(os.listdir(os.path.join(dir_path, TEST_RES_DIR_NAME)))
    