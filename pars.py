import datetime
from collections import namedtuple

import bs4
import requests

InnerBlock = namedtuple('Block', 'title, price, currency, date, url')

class Block(InnerBlock):
    def __str__(self):
        return f'{self.title}\t{self.price} {self.currency}\t{self.date}\t{self.url}'

class AvitoParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'accept': '*/*'
        }

    def get_page(self, page: int = None):
        params = {
            'cd': 1,
            'radius': 0,
        }
        if page and page > 1:
            params['p'] = page
        url = 'https://www.avito.ru/tver/doma_dachi_kottedzhi'
        r = self.session.get(url, params=params)
        return r.text