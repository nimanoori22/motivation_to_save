import requests
from bs4 import BeautifulSoup as bs
import re
import io

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
    
    def get_titles(self):
        soup = bs(self.page.content, 'html.parser')
        titles = (soup.select_one('.c-product__title-en').text,
        self.trim_persian_text(soup.select_one('.c-product__title').text))
        return titles

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


if __name__ == '__main__':

    link = 'https://www.digikala.com/product/dkp-3735138/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-13-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%D9%BE%D9%84-%D9%85%D8%AF%D9%84-macbook-air-mgn63-2020'
    link1 = 'https://www.digikala.com/product/dkp-2314622/%D9%87%D8%A7%D8%A8-3-%D9%BE%D9%88%D8%B1%D8%AA-usb-c-%D9%88%DB%8C%D9%88%D9%88-%D9%85%D8%AF%D9%84-c2h'
    dg = Digikala(link)

    print(dg.get_features())


