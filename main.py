import os

import requests
from environs import Env

from file_downloader import download_image


def parse_comic(comic_number):    
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url)
    return response.json()


def fetch_comics(local_files_dir, comic_number):
    comic_summary = parse_comic(comic_number)
    image_url = comic_summary['img']
    local_image_path = f'{local_files_dir}/comic_{comic_number}'
    download_image(image_url, local_image_path)


def main():
    env = Env()
    env.read_env()
    local_files_dir = env.str('LOCAL_FILES_DIR', 'Files')
    os.makedirs(local_files_dir, exist_ok=True)
    comic_number = '353'
    fetch_comics(local_files_dir, comic_number)


if __name__ == '__main__':
    main()