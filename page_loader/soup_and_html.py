from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import os
import re
import logging
from page_loader.files_and_dirs import save_file


def get_DOM(path):
    with open(path) as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
    return soup


def get_res_from_DOM(soup, root_url, res_kind):
    result = []
    tags = [t for t in soup.find_all(res_kind['tag']) if t.has_attr(res_kind['attr'])]
    root_uri = urlparse(root_url)
    for res in tags:
        if res[res_kind['attr']].startswith('http'):
            result.append(res[res_kind['attr']])
        elif res[res_kind['attr']].startswith('//'):
            result.append(
                root_uri.scheme + '://' + res[res_kind['attr']][2:]
            )
        else:
            root_url = root_url.rstrip('/')
            result.append(root_url + res[res_kind['attr']])
    logging.info(f"Got list of {res_kind['tag']}s to download. Number ={len(result)}")
    return result


def download_resours(res_list, dir_path):
    new_res_list = []
    for res in res_list:
        r = requests.get(res)
        full_path = urlparse(res).netloc + urlparse(res).path
        path, ext = os.path.splitext(full_path)
        save_path = re.sub(r'[^A-Za-z0-9]', r'-', path)
        save_path = os.path.join(dir_path, save_path + ext)
        logging.info(f'Saving asset to file {save_path}')
        save_file(save_path, 'wb', r.content)
        new_res_list.append(save_path)
    return new_res_list


def replace_resours(soup, res_list, res_kind):
    tags = [t for t in soup.find_all(res_kind['tag']) if t.has_attr(res_kind['attr'])]
    for i, tag in enumerate(tags):
        tag[res_kind['attr']] = res_list[i]
