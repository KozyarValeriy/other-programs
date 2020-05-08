"""
    Обединение файлов csv по городам в один общий файл.
"""

import pandas as pd
import os


def write_csv(data: set, file_name: str, column_name: str):
    """ Function to write csv data """
    tmp = pd.DataFrame(data, columns=[column_name])
    tmp.to_csv(file_name, index=False, header=False)


def is_mobile(number: int) -> bool:
    return str(number).startswith('79') or str(number).startswith('749')


def main():
    # get all files in directory
    files = os.listdir(path='.')
    # merge all files in one
    all_phones = set()
    num = 0
    # print('|{0: ^3s}|{1:<30s}{2:}|'.format('#'))
    for file in files:
        if file.endswith('.csv'):
            num += 1
            data = pd.read_csv(file, names=['phone'])
            data = data['phone'].values.tolist()
            all_phones.update(set(filter(is_mobile, data)))
            # all_phones = all_phones.merge(data, on='phone', how='outer')
            print('|№{0: >3d}|{1:.<30s}OK!|'.format(num, file.split('_')[0]))
    # write total file
    write_csv(all_phones, file_name='TOTAL_all_phones.csv', column_name='phone')


main()
