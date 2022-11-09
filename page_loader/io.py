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


def make_res_dir(dir_name, output):
    path = os.path.join(output, dir_name)
    logging.info('making dir for download resours ' + path)
    try:
        os.mkdir(path)
    except FileExistsError as e:
        logging.error(f'Dir {path} already exist!')
        print(f'Dir {path} already exist!')
        raise e
    logging.info(f'Dir {path} was successfully created')
