import requests
import logging
import os
from progress.bar import Bar
from page_loader.io import save_file, make_res_dir
from page_loader.url import to_dirname, to_filename
from page_loader.html import (
    get_parsed_html,
    prepare_res_list
)


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
            except FileExistsError:
                tag[attr] = url
                continue
            except PermissionError:
                tag[attr] = url
                continue
            bar.next()


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
