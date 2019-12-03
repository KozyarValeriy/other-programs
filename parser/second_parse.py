'''
Парсинг страницы https://yandextaxi.top/partner/ 
по всем городам для сбора номеров всех таксопарков по всем городам.
'''

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time

#constants parameters
url = r'https://yandextaxi.top/partner/'
#pattern city urls
pattern_city = url + r'([\w-]+)/'
pattern_page = r'page/(\d+)'
#pattern for phone like '78005110420'
pattern_phone_1 = r'[7|8][0-9]{10,10}' 
#pattern for phone like '+7 800 511-04-20'
pattern_phone_2 = r'\+?[7|8][ |-][0-9]{3,3}[ |-][0-9]{3,3}[ |-][0-9]{2,2}'\
                                                        r'[ |-][0-9]{2,2}'

def get_content(url: str, text: str) -> str:
    ''' Function to get page in str'''
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.select(text)
    return str(content)
    
def write_csv(data: set, file_name: str, column_name: str):
    ''' Function to write csv data '''
    tmp = pd.DataFrame(data, columns=[column_name])
    tmp.to_csv(file_name, index=False, header=False)

def main():
    ''' Main function. Collects all phones '''
    current_main_time = time.time() #start time
    content = get_content(url, text='ul#double')
    cities_names = re.findall(pattern_city, content)
    pos_moscow = cities_names.index('moskva')
    #city_to_url = dict()
    #html_to_str = get_content(url=url, class_=CITY_CLASS)
    #city_names = re.findall(pattern_city, html_to_str)
    #for city in city_names:
    #   if city.startswith('wp-'): continue
    #   city_to_url[city] = url + fr'{city}/'

    print('Number of cities: {0}'.format(len(cities_names)))
    print('|{0: ^3s}|{1: ^18s}|{2: ^7s}|{3: ^8s}|{4: ^8s}|'.format('№', 
                                        'City', 'Pages', 'Phones', 'Time'))
    print('|{0:-^3s}|{1:-^18s}|{2:-^7s}|{3:-^8s}|{4:-^8s}|'.format(
                                                         '', '', '', '', ''))
    #finding all phones in all cities
    all_phone = set()
    number = 0
    for city in cities_names[pos_moscow:]:
        number += 1
        current_time = time.time()
        #finding max page for all cities
        page_html = get_content(url=fr'{url}{city}/',
                                text='div.pagination.flex-row-center')
        page_numbers = re.findall(pattern_page, page_html)
        if page_numbers:
            max_page_num = max(int(page_number) for page_number in page_numbers)
        else:
            max_page_num = 1
        all_phones_in_city = set()
        
        for cur_page in range(1, max_page_num + 1):
            #for all page finding urls with taxi
            content_html = get_content(url=f'{url}{city}/page/{cur_page}/', 
                                       text='article.panel.panel-white')
            all_urls_page = re.findall(pattern_city, content_html)
            for curr_url in all_urls_page:
                #for all taxi
                if curr_url == city: continue
                content_html = get_content(url=f'{url}{curr_url}/', 
                                           text='table#taxi')
                phones = re.findall(pattern_phone_1, content_html)
                all_phones_in_city.update(set(phones))
            print('|{0: ^48s}|'.format(f'{city}: page {cur_page}/{max_page_num} done'))

        #pat = '|{0: ^4d}|{1.title()}| max page: {2:3d}| count_phones: {3:5d}|'
        print('|{0: ^3d}|{1: ^18s}|{2: ^7d}|{3: ^8d}|{4: ^8.2f}|'.format(number, city.capitalize(),
                                                              max_page_num, len(all_phones_in_city),
                                                              time.time()-current_time))
        #write phone and mail by city
        write_csv(all_phones_in_city, f'ordered_by_city/{city}_phone.csv', 'phone')
        all_phone.update(all_phones_in_city)
        
    print('All done, time escape: {:.1f}s'.format(time.time()-current_main_time))
    write_csv(all_phone, 'all_phone.csv', 'phone')

main()


'''
344
City: abakan              , max page:   3, count_phones:   34
City: azov                , max page:   1, count_phones:    9
City: akademgorodok       , max page:   1, count_phones:    1
City: alagir              , max page:   1, count_phones:    2
City: alapaevsk           , max page:   1, count_phones:    2
City: alatyr              , max page:   1, count_phones:    3
City: alejsk              , max page:   1, count_phones:    1
City: alekseevka          , max page:   1, count_phones:    1
City: aleksin             , max page:   1, count_phones:    3
City: almetevsk           , max page:   2, count_phones:   17
City: anapa               , max page:   4, count_phones:   44
City: angarsk             , max page:   1, count_phones:    9
City: anzhero-sudzhensk   , max page:   1, count_phones:    4
City: arzamas             , max page:   1, count_phones:    6
City: armavir             , max page:   2, count_phones:   28
City: artem               , max page:   2, count_phones:   17
City: arhangelsk          , max page:   1, count_phones:   14
City: asbest              , max page:   1, count_phones:    2
City: astrahan            , max page:   5, count_phones:   61
City: ahtubinsk           , max page:   1, count_phones:    1
City: achinsk             , max page:   1, count_phones:    6
City: asha                , max page:   1, count_phones:    3
City: balabanovo          , max page:   1, count_phones:    2
City: balakovo            , max page:   1, count_phones:   10
City: balashiha           , max page:   1, count_phones:   12
City: balashov            , max page:   1, count_phones:    1
City: barnaul             , max page:   7, count_phones:   98
City: batajsk             , max page:   1, count_phones:    1
City: bezenchuk           , max page:   1, count_phones:    2
City: belaya-kalitva      , max page:   1, count_phones:    2
City: belgorod            , max page:  10, count_phones:  145
City: beloretsk           , max page:   1, count_phones:    1
City: belorechensk        , max page:   1, count_phones:    1
City: belye-berega        , max page:   1, count_phones:    2
City: berdsk              , max page:   1, count_phones:    4
City: berezniki           , max page:   2, count_phones:   16
City: bii-sk              , max page:   1, count_phones:    9
City: bijsk               , max page:   1, count_phones:    6
City: birobidzhan         , max page:   1, count_phones:    3
City: biryuch             , max page:   1, count_phones:    1
City: blagoveshhensk      , max page:   4, count_phones:   96
City: bologoe             , max page:   1, count_phones:    2
City: borovichi           , max page:   1, count_phones:    2
City: bratsk              , max page:   1, count_phones:   17
City: bronnitsy           , max page:   1, count_phones:    2
City: bryansk             , max page:   5, count_phones:   73
City: buinsk              , max page:   1, count_phones:    3
City: bykovo              , max page:   1, count_phones:    1
City: valujki             , max page:   1, count_phones:    2
City: velikii-novgorod    , max page:   1, count_phones:   11
City: velikij-novgorod    , max page:   1, count_phones:   10
City: vladivostok         , max page:  10, count_phones:  134
City: vladikavkaz         , max page:   3, count_phones:   29
City: vladimir            , max page:   4, count_phones:   52
City: volgograd           , max page:  32, count_phones:  504
City: volgodonsk          , max page:   1, count_phones:   13
City: volgorechensk       , max page:   1, count_phones:    1
City: volzhsk             , max page:   1, count_phones:    1
City: volzhskii           , max page:   1, count_phones:    7
City: volzhskij           , max page:   2, count_phones:   17
City: vologda             , max page:   3, count_phones:   35
City: volokolamsk         , max page:   1, count_phones:    2
City: volsk               , max page:   1, count_phones:    8
City: voronezh            , max page:  12, count_phones:  159
City: voskresensk         , max page:   2, count_phones:   21
City: vyborg              , max page:   1, count_phones:   20
City: vyksa               , max page:   1, count_phones:    2
City: vyselki             , max page:   1, count_phones:    1
City: vyatskie-polyany    , max page:   1, count_phones:    1
City: gaj                 , max page:   1, count_phones:    2
City: gelendzhik          , max page:   1, count_phones:    8
City: georgievsk          , max page:   1, count_phones:    5
City: glazov              , max page:   1, count_phones:    3
City: groznyj             , max page:   1, count_phones:    2
City: gubaha              , max page:   1, count_phones:    1
City: derbent             , max page:   1, count_phones:   10
City: dzerzhinsk          , max page:   1, count_phones:   11
City: divnogorsk          , max page:   1, count_phones:    1
City: dimitrovgrad        , max page:   1, count_phones:   12
City: dmitrov             , max page:   2, count_phones:   26
City: dubna               , max page:   1, count_phones:   15
City: egorevsk            , max page:   1, count_phones:   11
City: ejsk                , max page:   1, count_phones:    2
City: ekaterinburg        , max page:  82, count_phones: 1256
City: elets               , max page:   1, count_phones:   11
City: elizovo             , max page:   1, count_phones:    1
City: essentuki           , max page:   1, count_phones:    4
City: zheleznogorsk       , max page:   1, count_phones:    5
City: zavitinsk           , max page:   1, count_phones:    1
City: zalukokoazhe        , max page:   1, count_phones:    3
City: zarai-sk            , max page:   1, count_phones:    1
City: zarajsk             , max page:   1, count_phones:    1
City: zvenigorod          , max page:   1, count_phones:    2
City: zelenokumsk         , max page:   1, count_phones:    2
City: ivanovo             , max page:   2, count_phones:   35
City: izhevsk             , max page:   5, count_phones:   80
City: i-oshkar-ola        , max page:   2, count_phones:   16
City: irkutsk             , max page:   6, count_phones:  119
City: istra               , max page:   1, count_phones:    9
City: ishim               , max page:   1, count_phones:    3
City: joshkar-ola         , max page:   1, count_phones:    9
City: kazan               , max page:  66, count_phones:  990
City: kalachinsk          , max page:   1, count_phones:    2
City: kaliningrad         , max page:  10, count_phones:  127
City: kaluga              , max page:   4, count_phones:   57
City: kamensk-uralskii    , max page:   1, count_phones:   10
City: kamensk-uralskij    , max page:   1, count_phones:    4
City: kamyzyak            , max page:   1, count_phones:    2
City: kamyshin            , max page:   1, count_phones:    6
City: kamyshlov           , max page:   1, count_phones:    1
City: kanash              , max page:   1, count_phones:    2
City: kansk               , max page:   1, count_phones:    1
City: karabudahkent       , max page:   1, count_phones:    2
City: karasuk             , max page:   1, count_phones:    2
City: kasimov             , max page:   1, count_phones:    2
City: kasli               , max page:   1, count_phones:    3
City: kaspijsk            , max page:   1, count_phones:    6
City: kashira             , max page:   1, count_phones:    5
City: kemerovo            , max page:   7, count_phones:   83
City: kirzhach            , max page:   1, count_phones:    1
City: kirishi             , max page:   1, count_phones:    2
City: kirov               , max page:   4, count_phones:   43
City: kirovo-chepetsk     , max page:   1, count_phones:    1
City: kislovodsk          , max page:   1, count_phones:    5
City: klin                , max page:   1, count_phones:   12
City: kovrov              , max page:   1, count_phones:   11
City: kogalym             , max page:   1, count_phones:    3
City: kozelsk             , max page:   1, count_phones:    2
City: kozmodemyansk       , max page:   1, count_phones:    1
City: kolomna             , max page:   2, count_phones:   30
City: kolchugino          , max page:   1, count_phones:    4
City: komsomolsk-na-amure , max page:   2, count_phones:   44
City: konakovo            , max page:   1, count_phones:    2
City: korolev             , max page:   1, count_phones:    2
City: korsakov            , max page:   1, count_phones:    1
City: kostroma            , max page:   1, count_phones:    9
City: krasnoarmei-sk      , max page:   1, count_phones:    1
City: krasnoarmejsk       , max page:   1, count_phones:    1
City: krasnobrodskij      , max page:   1, count_phones:    1
City: krasnodar           , max page:  70, count_phones: 1198
City: krasnoturinsk       , max page:   1, count_phones:    3
City: krasnoyarsk         , max page:  18, count_phones:  234
City: kumertau            , max page:   1, count_phones:    1
City: kungur              , max page:   1, count_phones:    2
City: kurgan              , max page:   2, count_phones:   24
City: kurovskoe           , max page:   1, count_phones:    3
City: kursavka            , max page:   1, count_phones:    1
City: kursk               , max page:   4, count_phones:   60
City: kurchatov           , max page:   1, count_phones:    3
City: kushhevskaya        , max page:   1, count_phones:    0
City: kyzyl               , max page:   1, count_phones:    3
City: labytnangi          , max page:   1, count_phones:    3
City: leninogorsk         , max page:   1, count_phones:    2
City: lesnoj              , max page:   1, count_phones:    1
City: likino-dulevo       , max page:   1, count_phones:    1
City: lipetsk             , max page:   6, count_phones:  138
City: liski               , max page:   1, count_phones:    3
City: luga                , max page:   1, count_phones:    2
City: lyubinskij          , max page:   1, count_phones:    1
City: magadan             , max page:   1, count_phones:    1
City: magas               , max page:   1, count_phones:    2
City: magnitogorsk        , max page:   3, count_phones:   55
City: majkop              , max page:   1, count_phones:   14
City: malaya-vishera      , max page:   1, count_phones:    2
City: malgobek            , max page:   1, count_phones:    2
City: maloyaroslavets     , max page:   1, count_phones:    2
City: matveev-kurgan      , max page:   1, count_phones:    2
City: mahachkala          , max page:   4, count_phones:   32
City: megion              , max page:   1, count_phones:    2
City: mednogorsk          , max page:   1, count_phones:    1
City: mezhdurechensk      , max page:   1, count_phones:    2
City: mesyagutovo         , max page:   1, count_phones:    1
City: miass               , max page:   2, count_phones:   32
City: mineralnye-vody     , max page:   1, count_phones:    3
City: mozhai-sk           , max page:   1, count_phones:    7
City: mozhajsk            , max page:   1, count_phones:   10
City: mozdok              , max page:   1, count_phones:    1

'''
