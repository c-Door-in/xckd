import logging
import os
from urllib.parse import urlsplit, unquote

import requests


logger = logging.getLogger('logger_main')


def parse_url_file_ext(url):
    path = unquote(urlsplit(url).path)
    return os.path.splitext(path)[1]


def download_image(url, image_path, params={}):
    response = requests.get(url, params=params)
    response.raise_for_status()
    ext = parse_url_file_ext(url)
    ext_image_path = f'{image_path}{ext}'
    with open(ext_image_path, 'wb') as file:
        file.write(response.content)
    return ext_image_path
