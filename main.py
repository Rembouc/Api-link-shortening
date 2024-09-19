import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


load_dotenv()


def shorten_link(token, long_url):
    url_method = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'access_token': token,
        'v': '5.199',
        'url': long_url
    }
    response = requests.get(url_method, params=params)
    response.raise_for_status()
    shorted_link = response.json()['response']['short_url']
    return shorted_link


def get_count_clicks(token, short_link):
    parsed_url = urlparse(short_link)
    url_method = ('https://api.vk.ru/method/utils.getLinkStats')
    params = {
        'access_token': token,
        'v': '5.199',
        'key': parsed_url.path[1:],
        'interval': 'forever'
    }
    response = requests.get(url_method, params=params)
    response.raise_for_status()
    count_clicks = response.json()['response']['stats'][0]['views']
    return count_clicks


def is_shorten_link(token, url):
    parsed_url = urlparse(url)
    url_method = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'v': '5.199',
        'key': parsed_url.path[1:],
        'interval': 'forever'
    }
    response = requests.get(url_method, params=params)
    response.raise_for_status()
    return 'error' not in response.text
 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='СОКРАЩАЕТ ССЫЛКИ'
    )
    parser.add_argument('-link', help='ВВЕДИТЕ ССЫЛКУ КОТОРУЮ НУЖНО СОКРАТИТЬ')
    args = parser.parse_args()
    print(args.link)
    link = args.link
    secret = os.getenv("SECRET_KEY")
    try:
        if is_shorten_link(secret, link):
            print('Короткая ссылка')
            clickers = get_count_clicks(secret, link)
            print('Количество кликов:', clickers)
        else:
            short_link = shorten_link(secret, link)
            print('Сокращенная ссылка: ', short_link)  
    except KeyError:
        print('Неверная ссылка')
