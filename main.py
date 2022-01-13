import logging
import os
from random import randint
from urllib.parse import urlsplit, unquote

import requests
from environs import Env

from file_downloader import download_image
from vk_post_image import post_image


logger = logging.getLogger(__name__)


def get_random_comic_number():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    total_comics = response.json()['num']
    return randint(1, total_comics)


def parse_random_comic():
    comic_number = get_random_comic_number()
    logger.info('Parsing comic %s', comic_number)
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()   
    return response.json()


def get_comic_image_path(image_url, files_dir):
    path = os.path.basename(unquote(urlsplit(image_url).path))
    return f'{files_dir}/{path}'


def main():
    logging.basicConfig(
        level=logging.INFO,
        format=(
            '%(asctime)s - %(name)s - '
            '%(levelname)s - %(funcName)s - %(message)s'
        ),
    )
    logger.info('Starting program')

    env = Env()
    env.read_env()
    files_dir = env.str('FILES_DIR', 'Files')
    vk_app_access_token = env.str('VK_APP_ACCESS_TOKEN')
    vk_group_id = env.str('VK_GROUP_ID')
    vk_version = env.str('VK_VERSION', '5.131')

    os.makedirs(files_dir, exist_ok=True)

    comic_summary = parse_random_comic()
    comic_image_url = comic_summary['img']
    comic_image_path = get_comic_image_path(comic_image_url, files_dir)
    download_image(comic_image_url, comic_image_path)
    
    comic_title = comic_summary['alt']
    try:
        post_image(
            vk_group_id,
            vk_app_access_token,
            vk_version,
            comic_image_path,
            comic_title,
        )
    finally:
        os.remove(comic_image_path)

if __name__ == '__main__':
    main()
