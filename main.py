import datetime
import time
from collections import namedtuple
import csv
import bs4
import requests

InnerBlock = namedtuple('Block', 'title, area, price, currency, date, address, url')
estate = []

URLAVITO = 'https://www.avito.ru'
URLRAZDEL = '/tver/doma_dachi_kottedzhi'
#URLRAZDEL = '/tver/zemelnye_uchastki'
#https://www.avito.ru/tver/zemelnye_uchastki
#https://www.avito.ru/tver/doma_dachi_kottedzhi
#https://www.avito.ru/tver/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?cd=1&f=ASgBAQECAUSUA9AQAUDYCDTMWcpZzlkCRZAJGHsiZnJvbSI6MTQ1NTUsInRvIjpudWxsfcATGHsiZnJvbSI6bnVsbCwidG8iOjE0NjM2fQ
#https://www.avito.ru/tver/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?q=%D0%B7%D0%B0%D1%82%D0%B2%D0%B5%D1%80%D0%B5%D1%87%D1%8C%D0%B5&f=ASgBAQICAUSUA9AQAUDYCDTMWcpZzlk
#https://www.avito.ru/tver/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?cd=1&district=308&f=ASgBAQECAUSUA9AQAUDYCDTMWcpZzlkBRZAJGHsiZnJvbSI6MTQ1NTUsInRvIjpudWxsfQ
#https://www.avito.ru/tver/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?cd=1&f=ASgBAQECAUSUA9AQAUDYCDTMWcpZzlkBRZAJGHsiZnJvbSI6MTQ1NTUsInRvIjpudWxsfQ
#https://www.avito.ru/tver/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?cd=1&q=%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9+%D1%81%D0%B2%D0%B5%D1%82
#https://www.avito.ru/tver/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?q=%D0%B8%D0%B3%D0%BD%D0%B0%D1%82%D0%BE%D0%B2%D0%BE

#URLRAZDEL = '/tver/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ'
#https://www.avito.ru/tver/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?f=ASgBAQICAUSUA9AQAUDYCDTOWcxZylk
#URLRAZDEL = '/tver/kvartiry/prodam/novostroyka-ASgBAQICAUSSA8YQAUDmBxSOUg'
FILE = 'estates.csv'


class Block(InnerBlock):
    def __str__(self):
        return f'{self.title}\t{self.area}\t{self.price} {self.currency}\t{self.date}\t{self.address}\t{self.url}'


class AvitoParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
        }

    def get_page(self, page: int = None):
        params = {
     #       'cd': 1,
            'district': 308,
    #Здесь написано "Затверечье"
            'q': '%D0%B7%D0%B0%D1%82%D0%B2%D0%B5%D1%80%D0%B5%D1%87%D1%8C%D0%B5',
    #Здесь написано Новый свет
    #        'q': '%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9+%D1%81%D0%B2%D0%B5%D1%82'
    #Здесь написано Игнатово
    #        'q':'%D0%B8%D0%B3%D0%BD%D0%B0%D1%82%D0%BE%D0%B2%D0%BE'
    #        'f': 'ASgBAQECAUSUA9AQAUDYCDTMWcpZzlkBRZAJGHsiZnJvbSI6MTQ1NTUsInRvIjpudWxsfQ',
    #        'f':'ASgBAQECAUSUA9AQAUDYCDTMWcpZzlkBRZAJGHsiZnJvbSI6MTQ1NTUsInRvIjpudWxsfQ'
   #         'radius': 0,
  #          'user': 1,
        }
        if page and page > 1:
            params['p'] = page

        url = URLAVITO + URLRAZDEL
        r = self.session.get(url, params=params)
        return r.text

    @staticmethod
    def parse_date(item: str):
        params = item.strip().split(' ')
        if len(params) == 2:
            day, time = params
            if day == 'Сегодня':
                date = datetime.date.today()
            elif day == 'Вчера':
                date = datetime.date.today() - datetime.timedelta(days=1)
            else:
                print('Непонятно когда:', item)
                return

            time = datetime.datetime.strftime(time, '%H:%M').time()
            return datetime.datetime.combine(date=date, time=time)
        elif len(params) == 3:
            day, month_hru, time = params
            day = int(day)
            months_map = {
                'января': 1,
                'февраля': 2,
                'марта': 3,
                'апреля': 4,
                'мая': 5,
                'июня': 6,
                'июля': 7,
                'августа': 8,
                'сентября': 9,
                'октября': 10,
                'ноября': 11,
                'декабря': 12,
            }
            month = months_map.get(month_hru)
            if not month:
                print('Непонятно какой месяц:', item)
                return
            today = datetime.datetime.today()
            time = datetime.datetime.strptime(time, '%H:%M')
            return datetime.datetime(day=day, month=month, year=today.year, hour=time.hour, minute=time.minute)
        else:
            print('Непонятный формат:', item)
            return

    def get_pagination_limit(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')
        last_page = None
        container = None
        container = soup.select('span.pagination-item-1WyVp')
        if container:
            last_button = container[-2]
            last_page = last_button.get_text()
        if not last_page:
            return 1
        else:

            return int(last_page)

    def save_file(self, estate, path):
        with open(path, 'w', newline='', encoding='UTF8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Наименование', 'Площадь', 'Цена', 'Дата', 'Адрес', 'Ссылка'])
            list(map(lambda x: writer.writerow([x['title'], x['area'], x['price'], x['date'], x['address'], x['url']]), estate))

    def get_blocks(self, page: int =None):
        text = self.get_page(page=page)
        soup = bs4.BeautifulSoup(text, 'lxml')

        # Запрос CSS-селектора, состоящего из множества классов, производится через select
        container = soup.select('div.snippet-horizontal.snippet-redesign.item.item_table.clearfix.js-catalog-item-enum.item-with-contact.js-item-extended')

        for item in container:
           block = self.parce_block(item=item)
           estate.append({
              'title': block.title,
               'area': block.area,
               'price': block.price,
               'date': block.date,
               'address': block.address,
               'url': block.url,
           })

        #estate = list(map(lambda x: self.parce_block(x), container))

        return estate

    def parce_block(self, item):
        #Выбрать блок со ссылкой
        url_block = item.select_one('a.snippet-link')
        href = url_block.get('href')
        if href:
            url = URLAVITO + href
        else:
            url = None

        # Выбрать блок с названием
        title_block = item.select_one('a.snippet-link span')
        title = title_block.string.strip()

        #Выбрать блок с площадью
        area_block = title.split('м²')[0]
        def numbs(x):
            if ('0' <= x <= '9') or (x == '.'):
                return 1
            else:
                return 0
        #print(area_block)
        area = 0.0
        if str(''.join(filter(numbs, area_block))):
            area = float(str(''.join(filter(numbs, area_block))).rstrip('.'))
            #area = float(''.join(filter(numbs, area_block)))

        # Выбрать блок с ценой и валютой
        price_block = item.select_one('span.snippet-price')
        price_block = price_block.get_text().split('₽')
        price_block = ''.join(price_block).split()
        price = 0.0
        if str(''.join(filter(str.isdigit, price_block))):
            price = float(''.join(filter(str.isdigit, price_block)))

        # выбрать блок с датой размещения
        date = None
        absolute_date = None
        date_block = item.select_one('div.snippet-date-info')
        absolute_date = date_block.get('data-tooltip')
        if absolute_date:
            date = self.parse_date(item=absolute_date)
            date = date.strftime('%d/%m/%Y')
        else:
            date = '22/11/63'

        address_block = item.select_one('span.item-address__string')
        address = address_block.string.strip()

        return Block(
            url=url,
            title=title,
            area=area,
            price=price,
            currency='₽',
            address=address,
            date=date,
        )

    def parce_all(self):
        limit = self.get_pagination_limit()
        first = 1
        print(f'Всего страниц: {limit}')
        estate = []
        for i in range(first, limit + 1):
            print('Обрабатываю страницу:', i)
            estate.extend(self.get_blocks(page=i))
            time.sleep(0.01)


def main():
   p = AvitoParser()
   p.parce_all()
   p.save_file(estate, FILE)

if __name__ == '__main__':
    main()
