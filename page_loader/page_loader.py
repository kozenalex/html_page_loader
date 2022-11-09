import requests
import logging
import os
from page_loader.io import save_file, make_res_dir
from page_loader.url import to_dirname, to_filename
from page_loader.resources import prepare_res_list
from page_loader.html import (
    get_parsed_html,
    download_resourses
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
    parsed_html = get_parsed_html(req.text)
    res_list = prepare_res_list(parsed_html, target_url)
    if res_list:
        resours_dir = to_dirname(target_url)
        make_res_dir(resours_dir, output)
        download_resourses(res_list, output, resours_dir, parsed_html)
    file_path = os.path.join(output, to_filename(target_url))
    logging.info('saving new html to file ' + file_path)
    save_file(file_path, 'w', parsed_html.prettify())
    logging.info('Job done!')
    return file_path
