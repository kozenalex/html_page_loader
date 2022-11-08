import requests
import logging
import os
from page_loader.io import (
    make_file_name,
    make_res_dir_name,
    save_file
)
from page_loader.html import (
    get_parsed_html,
    get_res_from_DOM,
    download_resours
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
    file_path = os.path.join(output, make_file_name(target_url))
    logging.info('saving html to file ' + file_path)
    save_file(file_path, 'wb', req.content)
    parsed_html = get_parsed_html(req.text)
    resours_dir = make_res_dir_name(file_path)
    res_list = get_res_from_DOM(parsed_html, target_url, resours_dir, output)
    download_resours(res_list)
    save_file(file_path, 'w', parsed_html.prettify())
    logging.info('Job done!')
    return file_path
