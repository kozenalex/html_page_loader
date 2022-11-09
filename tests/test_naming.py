from page_loader.url import to_filename
import pytest


CASES = [
    'https://ru.hexlet.io/',
    'https://ru.hexlet.io/courses',
    'http://ru.hexlet.io/courses/imgs/img.png',
    'http://ru.hexlet.io/scripts/script.js?1234&js=1234'
]


EXPECTED_NAMES = [
    'ru-hexlet-io.html',
    'ru-hexlet-io-courses.html',
    'ru-hexlet-io-courses-imgs-img.png',
    'ru-hexlet-io-scripts-script.js-1234-js-1234'
]


@pytest.mark.parametrize("case, expected", zip(CASES, EXPECTED_NAMES))
def test_to_filename(case, expected):
    assert to_filename(case) == expected
