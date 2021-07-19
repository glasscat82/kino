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
        
        # the paginator
        select_paginator = soup.find('main').find('div', class_='paginator')        
        paginator = []
        if select_paginator is not None:
            for a_ in select_paginator.find_all('a'):
                try:                
                    r_ = []
                    r_.append(a_.get('href'))
                    r_.append(a_.text.strip())
                    r_.append('active' if 'paginator__page-number_is-active' in a_.get('class') else '')                
                    paginator.append(r_)
                except Exception as e:
                    print(sys.exc_info()[1])
                    continue
            # self.p(paginator)

        return {'films':links, 'paginator':paginator}

    def get_afisha_city(self, html):
        if html is False:
            return False
        soup = BeautifulSoup(html, 'lxml')
        selection_list = soup.find_all('div', class_='showing')
        sked = []
        for in_, r_ in enumerate(selection_list, 1):
            try:                
                films_ = {}
                films_['node'] = in_
                films_['title'] = r_.find('div', class_='showDate').text.strip()
                flm_ = []
                for ind_, metro_ in enumerate(r_.find_all('div', class_='films_metro'), 1):
                    # the name film
                    title_ = metro_.find('div', {'class':'title _FILM_'})
                    name_ = title_.find('div').find('p').find('a')
                    href_ = name_.get('href')
                    # the description film
                    info_ = metro_.find('ul', {'class','film_info'})
                    description_ = [li_.text.strip() for li_ in info_.find_all('li')]
                    
                    # cinema and time
                    parsk_ = []
                    for cinema_ in metro_.find('div', {'class':'showing_section'}).find_all('dl'):
                        c_name = cinema_.find('dt', {'class':'name'}).text.strip()                                             
                        c_time = [t_.text.strip() for t_ in  cinema_.find('dd', {'class':'time'}).find_all(recursive=False)]
                        parsk_.append({'name':c_name, 'time':c_time})

                    # the json from films
                    flm_.append({'node':ind_, 'url':href_, 'name':name_.text.strip(), 'description':description_, 'cinema':parsk_})
                films_['films'] = flm_
                # ---                
                sked.append(films_)
            except Exception as e:
                print(sys.exc_info()[1])
                continue
        return sked

    def get_film(self, html):
        if html is False:
            return False
        soup = BeautifulSoup(html, 'lxml')
        selection_list = soup.find_all('div', {'class':'styles_root__3BHiJ'})
        flm = False
        for in_, r_ in enumerate(selection_list, 1):
            if in_ > 1:
                continue            
            try:
                film_body = r_.find('div', {'class':'styles_root__2jZrC'}, recursive=False)
                h1_ = film_body.find('h1').text.strip()
                h3_ = film_body.find('div', {'data-test-id':'encyclopedic-table'})
                descrip_ = []
                for d_ in h3_.findChildren("div" , recursive=False):
                    ds_ = [desc_.text.strip() for desc_ in d_.findChildren("div" , recursive=False)]
                    descrip_.append(ds_) 

                # ul.styles_list__I97eu
                flm = {'h1':h1_, 'description':descrip_}
                # self.p(h1_)
                # self.p(descrip_)

            except Exception as e:
                print(sys.exc_info()[1])
                continue
        
        return flm