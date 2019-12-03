'''
Парсинг страницы https://driver.yandex/ru-ru/base/parks
по всем городам для сбора номеров всех таксопарков по всем городам.
Города задаются черезу cookie.
'''

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time

#constants parameters
url = r'https://driver.yandex/ru-ru/base/parks'
#pattern for phone like '7999123456' or '88005553535'
pattern_phone_1 = r'[7|8][0-9]{10,10}' 
#pattern for phone like '+7 800 511-04-20'
pattern_phone_2 = r'\+?[7|8][ |-][0-9]{3,3}[ |-][0-9]{3,3}[ |-][0-9]{2,2}'\
														r'[ |-][0-9]{2,2}'
#pattern for mail
pattern_mail = r'[\w\.-]+@[\w\.-]+\.[\w\.-]+'

#reading dictionary city - cookie
def get_dict_city(file_name: str) -> dict:
	''' Function to readind csv file with [city,cookie] and 
		return dict(city:cookie)

		input data:
		file_name : name of csv file

		output data:
		result: dictionary with city keys and cookie values
	'''
	data = pd.read_csv(file_name, encoding="cp1251", index_col=None, sep=';')
	result = dict()
	for key, value in data.values:
		result[key] = str(value)
	return result

def write_csv(data: set, file_name: str, column_name: str):
	tmp = pd.DataFrame(data, columns=[column_name])
	tmp.to_csv(file_name, index=False, header=False)

def main():
	''' Main function. Collects all phones and mails '''
	current_time = time.time()
	cities_cookies = get_dict_city('city_cookie.csv')
	#cities_cookies = dict(Moscow='3', Abcan='104', Ekaterinburg='147')
	all_mail = set()
	all_phone = set()
	all_percents = len(cities_cookies)
	current = 0
	for city, cookie in cities_cookies.items():
		#get all page
		page = requests.get(url, cookies={'city':cookie}) 
		soup = BeautifulSoup(page.text, 'html.parser')
		first = soup.select('article#article_content')
		#finding all mail
		mails = re.findall(pattern_mail, str(first))
		mails = set(mail.lower() for mail in mails)
		#fainding all phones
		phones = re.findall(pattern_phone_1, str(first))
		phones += [phone.replace(' ', '').replace('+', '').replace('-', '') for \
							phone in re.findall(pattern_phone_2, str(first))]
		phones = set(phone.replace('8', '7', 1) if phone.startswith('8') 
											   else phone for phone in phones)
		#update main sets of mails and phones
		all_phone.update(phones)
		all_mail.update(mails)
		#write phone and mail by city
		write_csv(phones, f'ordered_by_city/{city}_phone.csv', 'phone')
		write_csv(mails, f'ordered_by_city/{city}_mail.csv', 'mail')
		current += 1
		print(f'Done {current}/{all_percents}')

	write_csv(all_phone, 'all_phone.csv', 'phone')
	write_csv(all_mail, 'all_mail.csv', 'mail')

	print('All done, time escape: {:.1f}s'.format(time.time()-current_time))

main()