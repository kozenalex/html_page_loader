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
    logging.info(f'File {path} was successfully saved')


def make_file_name(target_url):
    path, ext = os.path.splitext(target_url)
    file_name = re.sub(r'^http[s]*://', r'', path).rstrip('/')
    file_name = re.sub(r'[^A-Za-z0-9]', r'-', file_name)
    return file_name + ext if ext else file_name + '.html'


def make_res_dir_name(path):
    res = path.replace('.html', '_files')
    logging.info('making dir for download resours ' + res)
    try:
        os.mkdir(res)
    except FileExistsError as e:
        logging.error(f'Dir {res} already exist!')
        print(f'Dir {res} already exist!')
        raise e
    logging.info(f'Dir {res} was successfully created')
    return res


def compare_files(path1, path2):
    with open(path1, 'rb') as f1:
        comp1 = f1.read()
    with open(path2, 'rb') as f2:
        comp2 = f2.read()
    return comp1 == comp2
