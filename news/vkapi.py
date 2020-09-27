import json
import requests
from datetime import datetime

TOKEN = '084601db442ce57b45cf3cedf8ceed247ab49704686e2e0b11f305f4a89e98b9f9561d7c8b37d1a1defc8'
URL = 'https://api.vk.com/method/wall.get?&v=5.52'
DOMAIN = 'habr'

def get_request(count_posts=10):
    """
    Делает get запрос к API Vk через access_token и достаёт данные последних 10 постов группы domain
    """
    response = requests.get(URL, params={'access_token': TOKEN, 'domain': DOMAIN, 'offset': 0, 'count': count_posts})
    json_response = json.loads(response.text)
    publications = json_response['response']['items']
    response_list = get_items(response_items=publications)

    return response_list

def get_items(response_items):
    """
    Достаёт дату, текст поста и фотку_604 из каждого поста в response_items
    """
    response_list = []
    for items in response_items:
        date = datetime.fromtimestamp(items['date'])
        text = items['text']
        if 'attachments' in items:
            keys = items['attachments'][0].keys()
            for key in keys:
                if key == 'photo':
                    link_on_photo = check_on_key(items['attachments'][0])
                elif key == 'link':
                    link_on_photo = check_on_key(items['attachments'][0]['link'])
                else:
                    link_on_photo = False
            just_list = [date, text, link_on_photo]
            if not link_on_photo:
                pass
            else:
                response_list.append(just_list)
    return response_list

def check_on_key(check_dict):
    """
    Проверяет словарь по ключу photo и достаёт фотку_604
    """
    keys = check_dict.keys()
    for new_key in keys:
        if new_key == 'photo':
            if 'photo_604' in check_dict['photo']:
                link_on_photo = check_dict['photo']['photo_604']
            else:
                link_on_photo = False
            return link_on_photo




