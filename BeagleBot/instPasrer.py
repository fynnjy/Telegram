from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from instabot import Bot
import requests
import shutil
import json
import glob
import os


def new_instagram_user_creation(username, password):
    new_user = {
        'username': username,
        'password': str(password)
    }

    with open('Accounts/InstagramAccounts.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        data['Values'].append(new_user)

    with open('Accounts/InstagramAccounts.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_instagram_info(user):
    check_file = os.path.exists('Config')

    if check_file == True:
        file_path = 'Config'
        shutil.rmtree(file_path)
    else:
        None

    with open('Accounts/InstagramAccounts.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    username = data['Values'][0]['username']
    password = data['Values'][0]['password']

    bot = Bot()
    bot.login(username=username, password=password)

    all_instagram_info = bot.get_user_info(str(user))
    if type(all_instagram_info) == bool:
        return 'non-existent'

    else:
        user_media_count = all_instagram_info['media_count']
        user_followers = all_instagram_info['follower_count']
        user_following = all_instagram_info['following_count']
        user_biography = all_instagram_info['biography']

        user_info = {
            'username': user,
            'user_media_count': user_media_count,
            'user_followers': user_followers,
            'user_following': user_following,
            'user_biography': user_biography
        }

        with open('Dicts/new_instagram_user.json', 'w', encoding='utf-8') as file:
            json.dump(user_info, file, indent=4, ensure_ascii=False)


user = input('Input username: ')
get_instagram_info(user)



















