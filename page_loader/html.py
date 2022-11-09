import os.path
from bs4 import BeautifulSoup
from progress.bar import Bar
import requests
import logging
from page_loader.io import save_file
from page_loader.url import to_filename


def get_parsed_html(data):
    parsed_html = BeautifulSoup(data, 'html.parser')
    return parsed_html


def download_resourses(res_list, output, dir_name, p_html):
    with Bar('Downloading resourses:', max=len(res_list)) as bar:
        for res in res_list:
            url, tag, attr = res
            try:
                r = requests.get(url)
                r.raise_for_status()
                file_name = to_filename(url)
                save_path = os.path.join(output, dir_name, file_name)
                logging.info(f"Saving to file {save_path}")
                save_file(save_path, 'wb', r.content)
                tag[attr] = os.path.join(dir_name, file_name)
            except requests.ConnectionError:
                logging.warning(f"Could not download {url} - connection error")
                continue
            bar.next()
