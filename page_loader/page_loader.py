import requests
import re
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from page_loader.files_and_dirs import make_res_dir_name, save_file


def get_DOM(path):
    with open(path) as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
    return soup


def get_imgs_from_DOM(soup):
    res = []
    img_list = soup.find_all('img')
    for img in img_list:
        res.append(img['src'])
    return res


def download_imgs(img_list, dir_path):
    for img in img_list:
        r = requests.get(img)
        f_name = os.path.basename(urlparse(img).path)
        save_file(os.path.join(dir_path, f_name), 'wb', r.content)


def download(target_url, output):
    req = requests.get(target_url)
    file_name = re.sub(r'^http[s]*://', r'', target_url).rstrip('/')
    file_name = re.sub(r'[^A-Za-z0-9]', r'-', file_name) + '.html'
    path = os.path.join(output, file_name)
    save_file(path, 'wb', req.content)
    soup = get_DOM(path)
    img_list = get_imgs_from_DOM(soup)
    os.mkdir(make_res_dir_name(path))
    download_imgs(img_list, make_res_dir_name(path))
    return path
