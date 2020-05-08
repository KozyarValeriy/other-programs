"""
    Парсинг страницы https://yandextaxi.top/partner/
    по всем городам для сбора номеров всех таксопарков по всем городам.
"""

import re
import time

from bs4 import BeautifulSoup
import requests
import pandas as pd


# constants parameters
URL = r'https://yandextaxi.top/partner/'
# pattern city urls
pattern_city = URL + r'([\w-]+)/'
pattern_page = r'page/(\d+)'
# pattern for phone like '78005110420'
pattern_phone_1 = r'[7|8][0-9]{10,10}' 
# pattern for phone like '+7 800 511-04-20'
pattern_phone_2 = r'\+?[7|8][ |-][0-9]{3,3}[ |-][0-9]{3,3}[ |-][0-9]{2,2}[ |-][0-9]{2,2}'


def get_content(url: str, text: str) -> str:
    """ Function to get page in str"""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.select(text)
    return str(content)


def write_csv(data: set, file_name: str, column_name: str):
    """ Function to write csv data """
    tmp = pd.DataFrame(data, columns=[column_name])
    tmp.to_csv(file_name, index=False, header=False)


def main():
    """ Main function. Collects all phones """
    current_main_time = time.time()  # start time
    content = get_content(URL, text='ul#double')
    cities_names = re.findall(pattern_city, content)

    print('Number of cities: {0}'.format(len(cities_names)))
    print('|{0: ^3s}|{1: ^18s}|{2: ^7s}|{3: ^8s}|{4: ^8s}|'.format('№', 'City', 'Pages', 'Phones', 'Time'))
    print('|{0:-^3s}|{1:-^18s}|{2:-^7s}|{3:-^8s}|{4:-^8s}|'.format('', '', '', '', ''))
    # finding all phones in all cities
    all_phone = set()
    number = 0
    for city in cities_names:
        number += 1
        current_time = time.time()
        # finding max page for all cities
        page_html = get_content(url=fr'{URL}{city}/', text='div.pagination.flex-row-center')
        page_numbers = re.findall(pattern_page, page_html)
        if page_numbers:
            max_page_num = max(int(page_number) for page_number in page_numbers)
        else:
            max_page_num = 1
        all_phones_in_city = set()
        
        for cur_page in range(1, max_page_num + 1):
            # for all page finding urls with taxi
            content_html = get_content(url=f'{URL}{city}/page/{cur_page}/', text='article.panel.panel-white')
            all_urls_page = re.findall(pattern_city, content_html)
            for curr_url in all_urls_page:
                # for all taxi
                if curr_url == city:
                    continue
                content_html = get_content(url=f'{URL}{curr_url}/', text='table#taxi')
                phones = re.findall(pattern_phone_1, content_html)
                all_phones_in_city.update(set(phones))
            print('|{0: ^48s}|'.format(f'{city}: page {cur_page}/{max_page_num} done'))

        # pat = '|{0: ^4d}|{1.title()}| max page: {2:3d}| count_phones: {3:5d}|'
        print('|{0: ^3d}|{1: ^18s}|{2: ^7d}|{3: ^8d}|{4: ^8.2f}|'.format(number,
                                                                         city.capitalize(),
                                                                         max_page_num,
                                                                         len(all_phones_in_city),
                                                                         time.time() - current_time))
        # write phone and mail by city
        write_csv(all_phones_in_city, f'ordered_by_city/{city}_phone.csv', 'phone')
        all_phone.update(all_phones_in_city)
        
    print('All done, time escape: {:.1f}s'.format(time.time()-current_main_time))
    write_csv(all_phone, 'all_phone.csv', 'phone')


main()
