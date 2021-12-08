# Comics publisher
This application provides the publication of comics from the site [xkcd.com](https://xkcd.com/) in the social network [VKontakte](https://vk.com/).

Each launch will get the random comic from the source site. Then it will make a post at the wall of your existing VK public. It will post the comic image and its title as the post message.

## How to install
### Install requirements
Python3 should be installed already. Use command `pip` (or `pip3`, if there is a conflict with Python2) to install requirements:
```
pip install -r requirements.txt
```
### Prepare virtual environment
To use the application you need to obtain an `access token` for make posts on your VK public. Make sure that your access token has enough rights to publish a post with a photo on a public wall: `photos`, `groups`, `wall` and `offline`. Also, you should find out the current `VK version`. Learn more on [https://vk.com/dev](https://vk.com/dev).

Make `.env` file at the root of the project. Put variables there (use your values):
```
VK_GROUP_ID=[your public id]
VK_APP_ACCESS_TOKEN=[your access token]
VK_VERSION=[actual VK version]
```
*You can find your public ID at [regvk.com/id/](https://regvk.com/id/)*

You may set the name of a directory which will be created and where the comic image will save to before they upload to the VK server. After uploading, the file will be deleted.
```
LOCAL_FILES_DIR=[files_dir_name]
```
*It's "Files" by default*

## How to start
Launch `main.py` to start:
```
python main.py
```

## Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org).