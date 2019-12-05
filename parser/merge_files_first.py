'''
Обединение файлов csv по городам в один общий файл.
'''

import pandas as pd
import os

def write_csv(data: set, file_name: str, column_name: str):
    ''' Function to write csv data '''
    tmp = pd.DataFrame(data, columns=['City', column_name])
    tmp.to_csv(file_name, index=False, header=False, encoding='utf-8')

def is_mobile(number: int) -> bool:
	''' Check phone '''
	return str(number).startswith('79') or str(number).startswith('749')

def get_list(file_name: str, column_name: str, count: int):
	''' Method to collect all data by city '''
	data = pd.read_csv(file_name, names=[column_name])
	data = data[column_name].values.tolist()
	data = set(data)
	data = list(map((lambda x: (file_name.split('_')[0], x)), data))
	print('|№{0: >4d}|{1:.<50s}OK!|'.format(count, file_name.split('.')[0]))
	return data


def main():
	#get all files in directory
	files = os.listdir(path='.')
	#merge all files in one
	all_phones = []
	all_mail = []
	count = 0
	#print('|{0: ^3s}|{1:<30s}{2:}|'.format('#'))
	for file in files:
		if file.endswith('phone.csv'):
			count += 1
			all_phones += get_list(file, 'phone', count)
		elif file.endswith('mail.csv'):
			count += 1
			all_mail += get_list(file, 'mail', count)
	#write total file
	write_csv(all_phones, file_name='TOTAL_all_phones.csv', column_name='phone')
	write_csv(all_mail, file_name='TOTAL_all_mail.csv', column_name='mail')

main()
