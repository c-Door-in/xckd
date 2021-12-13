import logging
import os
from random import randint

import requests
from environs import Env

from file_downloader import download_image
from vk_post_image import post_image


logger = logging.getLogger('logger_main')


def get_random_comic_number():
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    total_comics = response.json()['num']
    return randint(1, total_comics)


def parse_comic(comic_number):
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_comic(files_dir):
    comic_number = get_random_comic_number()
    logger.debug(
        'Fetching comic %s to "%s" directory', comic_number, files_dir
    )
    comic_summary = parse_comic(comic_number)
    image_url = comic_summary['img']
    image_path = f'{files_dir}/comic_{comic_number}'
    image_ext_path = download_image(image_url, image_path)
    return comic_summary['alt'], image_ext_path


def main():
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
    )
    logger.setLevel(logging.DEBUG)
    logger.info('Starting program')

    env = Env()
    env.read_env()
    files_dir = env.str('FILES_DIR', 'Files')
    vk_app_access_token = env.str('VK_APP_ACCESS_TOKEN')
    vk_group_id = env.str('VK_GROUP_ID')
    vk_version = env.str('VK_VERSION')

    os.makedirs(files_dir, exist_ok=True)

    comic_title, comic_path = fetch_comic(files_dir)

    post_image(
        vk_group_id,
        vk_app_access_token,
        vk_version,
        comic_path,
        comic_title,
    )

    os.remove(comic_path)


if __name__ == '__main__':
    main()
