import logging

import requests
from environs import Env


logger = logging.getLogger('logger_main')


def get_wall_upload_server(group_id, app_access_token, version):
    logger.debug(
        'Getting wall upload server for vk group %s', group_id
    )
    method = 'photos.getWallUploadServer'
    url = f'https://api.vk.com/method/{method}'
    params = {
        'group_id': group_id,
        'access_token': app_access_token,
        'v': version,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    wall_upload_server_summary = response.json()
    if 'error' in wall_upload_server_summary:
        print(
            wall_upload_server_summary['error']['error_code'],
            wall_upload_server_summary['error']['error_msg'],
        )
        return
    return wall_upload_server_summary['response']['upload_url']


def upload_image(url, image_path):
    logger.debug(
        'Uploading image from %s to %s', url, image_path
    )
    with open(image_path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
    upload_summary = response.json()
    return upload_summary


def save_wall_photo(server, photo, hash, group_id, app_access_token, version):
    logger.debug(
        'Saving image to an album of the group %s', group_id
    )
    method = 'photos.saveWallPhoto'
    url = f'https://api.vk.com/method/{method}'
    data = {
        'server': server,
        'photo': photo,
        'hash': hash,
        'group_id': group_id,
        'access_token': app_access_token,
        'v': version,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    wall_photo_saving_summary = response.json()
    return wall_photo_saving_summary['response'][0]


def make_post(
            group_id,
            message,
            attach_type,
            attach_owner_id,
            attach_media_id,
            app_access_token,
            version,
        ):
    logger.debug(
        'Making post to the wall of the group %s with attaching of the %s',
        group_id,
        attach_type,
    )
    method = 'wall.post'
    url = f'https://api.vk.com/method/{method}'
    attachments = f'{attach_type}{attach_owner_id}_{attach_media_id}'
    data ={
        'owner_id': f'-{group_id}',
        'from_group': '1',
        'message': message,
        'attachments': attachments,
        'access_token': app_access_token,
        'v': version,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.text


def post_image(
            vk_group_id,
            vk_app_access_token,
            vk_version,
            image_path,
            message,
        ):
    logger.debug(
        'Posting comic from %s to vk group %s with message %s',
        image_path,
        vk_group_id,
        message,
    )
    wall_upload_server = get_wall_upload_server(
        vk_group_id,
        vk_app_access_token,
        vk_version,
    )

    upload_image_summary = upload_image(wall_upload_server, image_path)

    wall_photo_saving_summary = save_wall_photo(
        upload_image_summary['server'],
        upload_image_summary['photo'],
        upload_image_summary['hash'],
        vk_group_id,
        vk_app_access_token,
        vk_version,
    )

    attachment_type = 'photo'
    attachment_owner_id = wall_photo_saving_summary['owner_id']
    attachment_media_id = wall_photo_saving_summary['id']
    print(make_post(
        vk_group_id,
        message,
        attachment_type,
        attachment_owner_id,
        attachment_media_id,
        vk_app_access_token,
        vk_version,
    ))

    logger.debug('Posting complete')