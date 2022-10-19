def save_file(path, mode, content):
    with open(path, mode) as f:
        f.write(content)


def make_res_dir_name(path):
    res = path.replace('.html', '_files')
    return res
