import pytest
import requests
import requests_mock
import os
import tempfile
from page_loader import download
from page_loader.files_and_dirs import compare_files



TEST_URL = 'http://test.com/subdom/'
TEST_FILE_NAME = 'test-com-subdom.html'
TEST_RES_DIR_NAME = 'test-com-subdom_files'
FIXTURE_DIR = './tests/fixtures'
RESOURSES = (
    {'url': 'http://test.com/subdom/123.jpg', 'path': '123.jpg'},
    {'url': 'http://test.com/subdom/234.png', 'path': '234.png'},
    {'url': 'http://test.com/subdom/img/456.jpg', 'path': '456.jpg'},
    {'url': 'http://test.com/subdom/script.js', 'path': 'script.js'},
    {'url': 'http://test.com/subdom/style.css', 'path': 'style.css'}
)


def test_download():
    dir_path = tempfile.TemporaryDirectory().name
    os.mkdir(dir_path)
    f_name = os.path.join(dir_path, TEST_FILE_NAME)
    expected_files = []
    for i in RESOURSES:
        expected_files.append(os.path.join(FIXTURE_DIR, i['path']))
    with open(os.path.join(FIXTURE_DIR,'test.html')) as f:
        resp_text = f.read()
    with requests_mock.Mocker() as m:
        m.get(TEST_URL, text=resp_text)
        for i in RESOURSES:
            with open(os.path.join(FIXTURE_DIR, i['path']), 'rb') as f:
                r_content = f.read()
            m.get(i['url'], content=r_content)
        assert download(TEST_URL, dir_path) == f_name
    got_files = sorted(os.listdir(os.path.join(dir_path, TEST_RES_DIR_NAME)))
    assert len(expected_files) == len(got_files)
    for i, f in enumerate(expected_files):
        f1 = os.path.join(dir_path, TEST_RES_DIR_NAME, got_files[i])
        assert compare_files(f, f1) == True

    