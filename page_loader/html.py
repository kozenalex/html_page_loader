from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from progress.bar import Bar
import requests
import logging
from page_loader.io import save_file, make_file_name


RES_TAGS = [('img', 'src'), ('link', 'href'), ('script', 'src')]


def get_parsed_html(data):
    soup = BeautifulSoup(data, 'html.parser')
    return soup


def get_res_from_DOM(soup, root_url, save_dir, output):
    result = []
    parsed_url = urlparse(root_url)
    for res in RES_TAGS:
        type, attr = res
        tags = [t for t in soup.find_all(type) if t.has_attr(attr)]
        for tag in tags:
            parsed_src = urlparse(tag[attr])
            if parsed_src.netloc and parsed_url.netloc != parsed_src.netloc:
                continue
            elif tag[attr].startswith('http'):
                new_attr = tag[attr]
            else:
                new_attr = urljoin(root_url, tag[attr])
            save_path = save_dir + '/' + make_file_name(new_attr)
            result.append(
                {'url': new_attr, 'path': save_path}
            )
            tag[attr] = save_path.replace(output + '/', '')
    logging.info(f"Got list of resourses to download. Number ={len(result)}")
    return result


def download_resours(res_list):
    with Bar('Downloading resourses:', max=len(res_list)) as bar:
        for res in res_list:
            try:
                r = requests.get(res['url'])
                r.raise_for_status()
                logging.info(f"Saving to file {res['path']}")
                save_file(res['path'], 'wb', r.content)
            except requests.ConnectionError:
                logging.warning(f"Could not download {res['url']} - connection error")
                continue
            bar.next()
