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


def get_imgs_from_DOM(soup, root_url):
    res = []
    img_list = soup.find_all('img')
    for img in img_list:
        if urlparse(img['src']).netloc:
            res.append(img['src'])
        else:
            root_url = root_url.rstrip('/')
            res.append(root_url + img['src'])
    return res


def download_imgs(img_list, dir_path):
    new_img_list = []
    for img in img_list:
        r = requests.get(img)
        full_path = urlparse(img).netloc + urlparse(img).path
        path, ext = os.path.splitext(full_path)
        save_path = re.sub(r'[^A-Za-z0-9]', r'-', path)
        save_path = os.path.join(dir_path, save_path + ext)
        save_file(save_path, 'wb', r.content)
        new_img_list.append(save_path)
    return new_img_list


def replace_img(soup, imgs):
    for i, tag in enumerate(soup.find_all('img')):
        tag['src'] = imgs[i]


def download(target_url, output):
    req = requests.get(target_url)
    file_name = re.sub(r'^http[s]*://', r'', target_url).rstrip('/')
    file_name = re.sub(r'[^A-Za-z0-9]', r'-', file_name) + '.html'
    path = os.path.join(output, file_name)
    save_file(path, 'wb', req.content)
    soup = get_DOM(path)
    img_list = get_imgs_from_DOM(soup, target_url)
    os.mkdir(make_res_dir_name(path))
    new_img_list = download_imgs(img_list, make_res_dir_name(path))
    replace_img(soup, new_img_list)
    save_file(path, 'w+', soup.prettify())
    return path
