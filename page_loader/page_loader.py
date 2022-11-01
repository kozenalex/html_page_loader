import requests
import logging
import os
from page_loader.files_and_dirs import (
    make_file_name,
    make_res_dir_name,
    save_file
)
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


def download(target_url, output=os.getcwd):
    logging.info('Application started...')
    logging.info('trying to request ' + target_url)
    try:
        req = requests.get(target_url)
        req.raise_for_status()
    except requests.ConnectionError as e:
        logging.error(f'{e}')
        print(f'Could not connect, {e}')
        raise e
    file_path = make_file_name(target_url, output)
    logging.info('saving html to file ' + file_path)
    save_file(file_path, 'wb', req.content)
    soup = get_DOM(file_path)
    resours_dir = make_res_dir_name(file_path)
    for res_kind in RES_TAGS:
        res_list = get_res_from_DOM(soup, target_url, res_kind)
        new_res_list = download_resours(res_list, resours_dir, res_kind['tag'])
        replace_resours(soup, new_res_list, res_kind, output)
    save_file(file_path, 'w', soup.prettify())
    logging.info('Job done!')
    return file_path
