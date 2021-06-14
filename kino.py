# https://www.kinopoisk.ru/lists/navigator/?tab=all&page=1
import sys
import requests, fake_useragent  # pip install requests
import json
import re
from bs4 import BeautifulSoup

class kino():
    """parsing kinopoisk.ru for Russia"""
    def __init__ (self, url="https://www.kinopoisk.ru/lists/navigator/?tab=all&page=1", filename="kino.json"):
        self.url = url
        self.filename = filename    

    @staticmethod
    def p(text, *args):
        print(text, *args, sep=' / ', end='\n')

    def write_json(self, data, path = None):
        path = self.filename if path is None else path
        with open(path, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_json(self, path = None):
        path = self.filename if path is None else path
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
        return {}  

    # Random User-Agent
    def get_html(self, url_page = None):
        ua = fake_useragent.UserAgent() 
        user = ua.random
        header = {'User-Agent':str(user)}
        url_page = self.url if url_page is None else url_page
        try:
            page = requests.get(url_page, headers = header, timeout = 10)
            return page.text
        except Exception as e:
            print(sys.exc_info()[1])
            return False

    def get_all_links(self, html):
        if html is False:
            return False
        soup = BeautifulSoup(html, 'lxml')
        selection_list = soup.find('div', class_='selection-list')        
        # self.p(selection_list)

        # the for
        links = []
        for row_ in selection_list.find_all('div', class_='desktop-seo-selection-film-item selection-list__film'):
            # add field from film 
            try:
                a_ = row_.find('a', class_='selection-film-item-meta__link').get('href')
                poster_ = row_.find('img', class_='selection-film-item-poster__image').get('src')
                name_ = row_.find('p',class_='selection-film-item-meta__name').text.strip()
                original_ = row_.find('p',class_='selection-film-item-meta__original-name').text.strip()
                additional_ = row_.find('p',class_='selection-film-item-meta__meta-additional').text.strip()
                rating_ = row_.find('span',class_='rating__value').text.strip()
                rating_count_ = row_.find('span',class_='rating__count').text.strip().replace(' ', '')
                # self.p(name_)

                row = []
                row.append(a_)
                row.append(poster_)
                row.append(name_)
                row.append(original_)
                row.append(additional_)
                row.append(rating_)
                row.append(rating_count_)
                links.append(row)
            except Exception as e:
                print(sys.exc_info()[1])
                continue
        
        return links