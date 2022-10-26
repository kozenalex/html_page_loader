import requests
import re
import os
import logging
from page_loader.files_and_dirs import make_res_dir_name, save_file
from page_loader.soup_and_html import (
    get_DOM,
    get_res_from_DOM,
    download_resours,
    replace_resours
)


RES_TAGS = (
    {'tag': 'img', 'attr': 'src'},
    {'tag': 'link', 'attr': 'href'},
    {'tag': 'script', 'attr': 'src'}
)


def download(target_url, output):
    logging.info('Application started...')
    logging.info('trying to request ' + target_url)
    req = requests.get(target_url)
    file_name = re.sub(r'^http[s]*://', r'', target_url).rstrip('/')
    file_name = re.sub(r'[^A-Za-z0-9]', r'-', file_name) + '.html'
    path = os.path.join(output, file_name)
    logging.info('saving html to file ' + path)
    save_file(path, 'wb', req.content)
    soup = get_DOM(path)
    resours_dir = make_res_dir_name(path)
    logging.info('making dir for download resours ' + resours_dir)
    os.mkdir(resours_dir)
    for res_kind in RES_TAGS:
        print(f"Downloading {res_kind['tag']}s...")
        res_list = get_res_from_DOM(soup, target_url, res_kind)
        new_res_list = download_resours(res_list, resours_dir)
        replace_resours(soup, new_res_list, res_kind)
        print('Done!')
    save_file(path, 'w', soup.prettify())
    logging.info('Job done!')
    return path
