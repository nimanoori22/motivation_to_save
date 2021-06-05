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
    
    def get_features(self):
        soup = bs(self.page.content, 'html.parser')
        features = soup.select_one('.js-is-expandable ul')
        ul_soup = bs(str(features), 'html.parser').findAll('li')
        #strips white space inside and outside of string
        lis = [re.sub(' +', ' ', li.text.strip().replace('\n', '')) for li in ul_soup]
        return lis


if __name__ == '__main__':

    link = 'https://www.digikala.com/product/dkp-3735138/%D9%84%D9%BE-%D8%AA%D8%A7%D9%BE-13-%D8%A7%DB%8C%D9%86%DA%86%DB%8C-%D8%A7%D9%BE%D9%84-%D9%85%D8%AF%D9%84-macbook-air-mgn63-2020'
    dg = Digikala(link)

    print(dg.get_features())
