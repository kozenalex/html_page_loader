def save_file(path, mode, content):
    with open(path, mode) as f:
        f.write(content)


def make_res_dir_name(path):
    res = path.replace('.html', '_files')
    return res


def is_rel_path(path: str) -> bool:
    return path.startswith('./')


def compare_files(path1, path2):
    with open(path1, 'rb') as f1:
        comp1 = f1.read()
    with open(path2, 'rb') as f2:
        comp2 = f2.read()
    return comp1 == comp2
