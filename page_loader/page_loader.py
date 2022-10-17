import requests
import os
import re


def download(target_url, output):
    req = requests.get(target_url)
    file_name = re.sub(r'^http[s]*://', r'', target_url)
    file_name = re.sub(r'[^A-Za-z0-9]', r'-', file_name)
    file_name = os.path.join(output, file_name + '.html')
    with open(file_name, 'w+') as f:
        f.write(req.text)
    return file_name
