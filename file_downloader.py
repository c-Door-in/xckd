import logging
import os
from urllib.parse import urlsplit, unquote

import requests


logger = logging.getLogger('logger_main')


def download_image(url, image_path, params={}):
    response = requests.get(url, params=params)
    response.raise_for_status()
    logger.debug(
        'Download file from "%s" as %s', url, image_path
    )
    with open(image_path, 'wb') as file:
        file.write(response.content)
    return
