import logging

import requests

from file_uploader import upload_image


logger = logging.getLogger(__name__)


def vk_http_error_handler(response_summary):
    if 'error' in response_summary:
        raise requests.HTTPError(
            response_summary['error']['error_code'],
            response_summary['error']['error_msg'],
        )


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
    vk_http_error_handler(wall_upload_server_summary)
    return wall_upload_server_summary['response']['upload_url']


def save_wall_photo(server, photo, photo_hash, group_id, app_access_token, version):
    logger.debug(
        'Saving image to an album of the group %s', group_id
    )
    method = 'photos.saveWallPhoto'
    url = f'https://api.vk.com/method/{method}'
    payload = {
        'server': server,
        'photo': photo,
        'hash': photo_hash,
        'group_id': group_id,
        'access_token': app_access_token,
        'v': version,
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    wall_photo_saving_summary = response.json()
    vk_http_error_handler(wall_photo_saving_summary)
    return wall_photo_saving_summary['response'][0]


def make_post(
            group_id,
            message,
            attachment_type,
            attachment_owner_id,
            attachment_media_id,
            app_access_token,
            version,
        ):
    logger.debug(
        'Making post to the wall of the group %s with attaching of the %s',
        group_id,
        attachment_type,
    )
    method = 'wall.post'
    url = f'https://api.vk.com/method/{method}'
    attachments = f'{attachment_type}{attachment_owner_id}_{attachment_media_id}'
    payload = {
        'owner_id': f'-{group_id}',
        'from_group': '1',
        'message': message,
        'attachments': attachments,
        'access_token': app_access_token,
        'v': version,
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    post_summary = response.json()
    vk_http_error_handler(post_summary)
    logger.debug('Response is %s', response.text)
    return post_summary['response']['post_id']


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

    uploading_image_summary = upload_image(wall_upload_server, image_path)
    vk_http_error_handler(uploading_image_summary)

    wall_photo_saving_summary = save_wall_photo(
        uploading_image_summary['server'],
        uploading_image_summary['photo'],
        uploading_image_summary['hash'],
        vk_group_id,
        vk_app_access_token,
        vk_version,
    )

    attachment_type = 'photo'
    attachment_owner_id = wall_photo_saving_summary['owner_id']
    attachment_media_id = wall_photo_saving_summary['id']
    post_id = make_post(
        vk_group_id,
        message,
        attachment_type,
        attachment_owner_id,
        attachment_media_id,
        vk_app_access_token,
        vk_version,
    )

    logger.info('Posting complete. Post_id is %s', post_id)
