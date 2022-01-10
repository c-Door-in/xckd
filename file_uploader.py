import logging

import requests


logger = logging.getLogger(__name__)


def upload_image(url, image_path):
    logger.debug(
        'Uploading image from %s to %s', image_path, url
    )
    with open(image_path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
    response.raise_for_status()
    upload_summary = response.json()
    return upload_summary
