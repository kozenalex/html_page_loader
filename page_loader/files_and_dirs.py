import re
import os
import logging


def save_file(path, mode, content):
    try:
        with open(path, mode) as f:
            f.write(content)
    except PermissionError as e:
        logging.error(e)
        print(f'Permissions denied to save to {path}')
        raise e
    except FileNotFoundError as e:
        logging.error(e)
        print(f'Path not found {path}')
        raise e


def make_file_name(target_url, output):
    file_name = re.sub(r'^http[s]*://', r'', target_url).rstrip('/')
    file_name = re.sub(r'[^A-Za-z0-9]', r'-', file_name) + '.html'
    path = os.path.join(output, file_name)
    return path


def make_res_dir_name(path):
    res = path.replace('.html', '_files')
    logging.info('making dir for download resours ' + res)
    try:
        os.mkdir(res)
    except FileExistsError as e:
        logging.error(f'Dir {res} already exist!')
        print(f'Dir {res} already exist!')
        raise e
    return res


def is_rel_path(path: str) -> bool:
    return path.startswith('./')


def compare_files(path1, path2):
    with open(path1, 'rb') as f1:
        comp1 = f1.read()
    with open(path2, 'rb') as f2:
        comp2 = f2.read()
    return comp1 == comp2
