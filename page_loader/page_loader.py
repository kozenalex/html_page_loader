import requests
import re
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from page_loader.files_and_dirs import make_res_dir_name, save_file


RES_TAGS = (
    {'tag': 'img', 'attr': 'src'},
    {'tag': 'link', 'attr': 'href'},
    {'tag': 'script', 'attr': 'src'}
)


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
    return result


def download_resours(res_list, dir_path):
    new_res_list = []
    for res in res_list:
        r = requests.get(res)
        full_path = urlparse(res).netloc + urlparse(res).path
        path, ext = os.path.splitext(full_path)
        save_path = re.sub(r'[^A-Za-z0-9]', r'-', path)
        save_path = os.path.join(dir_path, save_path + ext)
        save_file(save_path, 'wb', r.content)
        new_res_list.append(save_path)
    return new_res_list


def replace_resours(soup, res_list, res_kind):
    tags = [t for t in soup.find_all(res_kind['tag']) if t.has_attr(res_kind['attr'])]
    for i, tag in enumerate(tags):
        tag[res_kind['attr']] = res_list[i]


def download(target_url, output):
    req = requests.get(target_url)
    file_name = re.sub(r'^http[s]*://', r'', target_url).rstrip('/')
    file_name = re.sub(r'[^A-Za-z0-9]', r'-', file_name) + '.html'
    path = os.path.join(output, file_name)
    save_file(path, 'wb', req.content)
    soup = get_DOM(path)
    resours_dir = make_res_dir_name(path)
    os.mkdir(resours_dir)
    for res_kind in RES_TAGS:
        print(f"Downloading {res_kind['tag']}s...")
        res_list = get_res_from_DOM(soup, target_url, res_kind)
        new_res_list = download_resours(res_list, resours_dir)
        replace_resours(soup, new_res_list, res_kind)
        print('Done!')
    save_file(path, 'w+', soup.prettify())
    return path
