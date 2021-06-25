from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup as bs
import re

class Digikala:
    def __init__(self, link):
        self.link = link
        self.page = requests.get(self.link)
    
    def get_pic(self):
        soup = bs(self.page.content, 'html.parser')
        pic_link = soup.select_one('.js-gallery-img')['data-src']
        return pic_link

    def get_price(self):
        soup = bs(self.page.content, 'html.parser')
        price = soup.select_one('.js-price-value')
        return price.text.strip()
    
    def get_title(self):
        soup = bs(self.page.content, 'html.parser')
        return self.trim_persian_text(soup.select_one('.c-product__title').text)

    def get_features(self):
        soup = bs(self.page.content, 'html.parser')
        features = soup.select_one('.js-is-expandable ul')
        ul_soup = bs(str(features), 'html.parser').findAll('li')
        #strips white space inside and outside of string
        lis = [self.trim_persian_text(li.text) for li in ul_soup]
        return lis

    def price_to_int(self):
        eng_num = ''
        price = self.get_price()
        nums = {
            '۱': 1, '۲': 2, '۳': 3,
            '۴': 4, '۵': 5, '۶': 6, '۷': 7, '۸': 8,
            '۹': 9, '۰': 0 
        }
        for i in price:
            if i in nums.keys():
                eng_num += str(nums[i])
        return int(eng_num)

    def trim_persian_text(self, text):
        return re.sub(' +', ' ', text.strip().replace('\n', ''))

class Command(BaseCommand):
    help = "collect jobs"
    # define logic of command
    def handle(self, *args, **options):
        pass
