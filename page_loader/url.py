import re
import os.path


def to_filename(target_url):
    path, ext = os.path.splitext(target_url)
    file_name = re.sub(r'^http[s]*://', r'', path).rstrip('/')
    file_name = re.sub(r'[^A-Za-z0-9]', r'-', file_name)
    ext = re.sub(r'[^A-Za-z0-9\.]', r'-', ext)
    return file_name + ext if ext else file_name + '.html'


def to_dirname(target_url):
    return to_filename(target_url).replace('.html', '_files')
