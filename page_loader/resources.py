import logging
from urllib.parse import urljoin, urlparse


RES_TAGS = [('img', 'src'), ('link', 'href'), ('script', 'src')]


def prepare_res_list(parsed_html, root_url):
    result = []
    parsed_url = urlparse(root_url)
    for res in RES_TAGS:
        type, attr = res
        tags = [t for t in parsed_html.find_all(type) if t.has_attr(attr)]
        for tag in tags:
            parsed_src = urlparse(tag[attr])
            if parsed_src.netloc and parsed_url.netloc != parsed_src.netloc:
                continue
            elif tag[attr].startswith('http'):
                new_attr = tag[attr]
            else:
                new_attr = urljoin(root_url, tag[attr])
            result.append(
                (new_attr, tag, attr)
            )
    logging.info(f"Got list of resourses to download. Number ={len(result)}")
    return result
