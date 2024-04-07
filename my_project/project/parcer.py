from bs4 import BeautifulSoup as bs
import requests
import fake_useragent
import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")

class Parser:

    def __init__(self, request):
        self.url = 'https://ural.toys/catalog/search/' + request
        self.user_agent = fake_useragent.UserAgent()
        self.user = self.user_agent.random
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': str(self.user),
            'Accept-Language': 'ru'
        }
        r = self.session.get(self.url, headers={'User-Agent': str(self.user)})
        self.html = r.text
        self.html_list = []
        self.html_list.append(self.html)

    def get_html_by_link(self, url):
        user_agent = fake_useragent.UserAgent()
        user = user_agent.random
        session = requests.Session()
        session.headers = {
            'User-Agent': str(user),
            'Accept-Language': 'ru'
        }
        r = session.get(url, headers={'User-Agent': str(user)})
        return r.text

    def all_links(self):
        all_links = []
        for html in self.html_list:
            soup = bs(html, 'lxml')
            ads = ''
            try:
                ads = soup.find('div', class_='c-list__wrap').find('div', class_='c-list__list').find_all('div', class_='c-list__item card')
            except Exception:
                logging.error("Страница по запросу не найдена")
            for ad in ads:
               link = 'https://ural.toys' + ad.find('div', class_='card__inner').find('a').get('href')
               all_links.append(link)
        return all_links

    def get_page_data(self, html, url):
        soup = bs(html, 'lxml')
        try:
            title = (soup.find('section', class_='product container')
                     .find("div", class_='product__wrap')
                     .find('div', class_='product__description-section').find('h1')
                     .get_text(strip='\n'))
        except Exception:
            title = 'Нет информации о названии'
        try:
            brand_name = (soup.find('section', class_='product container')
                          .find("div", class_='product__wrap')
                          .find('div', class_='product__description-section')
                          .find('div', class_='product__top')
                          .find('p', class_='product__mark product__gray')
                          .find('a', itemprop='brand').get_text(strip='\n'))

        except Exception:
            brand_name = 'Нет информации о бренде'
        data = {'title': title, 'brand_name': brand_name, 'url': url}
        return data


def parcer_start(title):

    start = Parser(title)
    all_links = start.all_links()
    cnt_link = len(all_links)
    data = []
    for link in all_links:
        html = start.get_html_by_link(link)
        data.append(start.get_page_data(html, link))
    return data, cnt_link
