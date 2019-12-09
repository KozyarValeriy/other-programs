"""
--------- Задание ---------
Реализация хэш-таблицы с открытой адресацией.
Операции: вставка, удаление, изменение.
Сделать тест с анализом времени работы при вставке/поиске в
зависимости от объема данных.
--------- Описание и тесты ---------
Реализация хэш-таблицы с открытой адресацией.
Реализует методы вставки, поиска и удаления элементов.
При реализации использовалось два списка:
self.__keys - для хранения ключей
self.__values - для зранения значений
Таким образом, при поиске ищеется ключ в списке ключей и, при наличии ключа,
возвращается значение из списка значений под тем же индексом.
Также работает и вставка: если ячейка в списке ключей свободна, то ключ
помещается на этот индекс, и на этот же индекс помещается значение в списке
значений.
>>> table = HashTable(11)
>>> table.size
11
>>> table['start'] = 194
>>> table[123] = 'value'
>>> table['house'] = 'white'
>>> table.values
[None, None, 194, 'value', 'white', None, None, None, None, None, None]
>>> table['house']
'white'
>>> del table['house']
>>> table.values
[None, None, 194, 'value', '!#!#!', None, None, None, None, None, None]
>>> table.values = [1, 4]
Traceback (most recent call last):
...
AttributeError: can't set attribute
"""


class OverflowTable(Exception): pass  # исключение для переполнения таблицы


class EmptyTable(Exception): pass  # исключение для пустой таблицы


class HashTable:

    def __init__(self, size: int = 997):
        """ Constructor
        >>> table = HashTable(3)
        >>> table.size
        3
        >>> table.values
        [None, None, None]
        """
        self.__keys = [None] * size
        self.__values = [None] * size
        self.__size = size
        self.__fill = 0

    def __getitem__(self, key):
        """ Метод для получения значения """
        return self.get(key)

    def __setitem__(self, key, value):
        """ Метод для установки значения по ключю """
        self.put(key, value)

    def __delitem__(self, key):
        ''' Метод удаления элемента по ключю '''
        self.remove(key)

    @property
    def size(self):
        return self.__size

    @property
    def values(self):
        return self.__values

    @property
    def keys(self):
        return self.__keys

    def __hash_function(self, key):
        """ Хэш-функция
        Для строк: если строка меньше 6 элементов, то считается сумма
        произведения номера символа на номер в слове, начиная с 1, а
        для длинного слова - сумма произведения последенего, среднего и
        первого символа на номер позиции, начиная с 1.
        затем берется остаток от деления на размер таблицы.
        Для чисел: берется остаток от деления на размер таблицы.
        """
        hash_val = 0
        if isinstance(key, str):
            if len(key) <= 5:
                hash_val = sum(ord(key[i]) * (i + 1) for i in range(len(key)))
            else:
                hash_val = sum(ord(key[i]) * (i + 1) for i in (len(key) - 1,
                                                               len(key) // 2, 0))
        elif isinstance(key, int):
            hash_val = key
        return hash_val % self.__size

    def __rehash(self, old_hash):
        """ Метод для увеличения хэша на 1 при коллизии """
        return (old_hash + 1) % self.__size

    def put(self, key, value, *args, hash_new=None, first=True, **kargs):
        """ Запись элемента в таблицу
        Так как реализована таблица с открытой адресацией, то при наступлении
        коллизии береться из метода __rehash следующее значение хеша и идет
        до тех пор, пока не найдет этот ключ или пустую ячейку.
        Если таблица заполнена, то возбуждает исключение OverflowTable.
        >>> table = HashTable(11)
        >>> table['cat'] = 'Hash is 3'
        >>> table[124] = 'Hash is 3'
        >>> table.values
        [None, None, None, 'Hash is 3', 'Hash is 3', None, None, None, None, None, None]
        >>> table['!#!#!'] = 'new_value'
        Traceback (most recent call last):
        ...
        ValueError: Invalid key
        >>> for i in range(9): table[i] = i
        >>> table[555] = 'new_value'
        Traceback (most recent call last):
        ...
        OverflowTable: Impossible to insert object. Table is full
        """
        if self.__fill >= self.__size:
            raise OverflowTable('Impossible to insert object. Table is full')
        if key == '!#!#!':
            raise ValueError('Invalid key')
        hash_val = self.__hash_function(key) if hash_new is None else hash_new
        # если новое значение
        if (self.__values[hash_val] is None):
            self.__values[hash_val] = value
            self.__keys[hash_val] = key
            self.__fill += 1
        # если такой ключ уже есть
        elif (self.__keys[hash_val] == key):
            self.__values[hash_val] = value
            self.__keys[hash_val] = key
        # если пришли второй раз и не нашли такого значения
        elif (self.__keys[hash_val] == '!#!#!' and not first):
            self.__values[hash_val] = value
            self.__keys[hash_val] = key
            self.__fill += 1
        else:
            start_hash = hash_val
            hash_val = self.__rehash(start_hash)
            while (self.__keys[hash_val] is not None and
                   self.__keys[hash_val] != key and
                   start_hash != hash_val and
                   (self.__keys[hash_val] != '!#!#!' and not first)):
                hash_val = self.__rehash(hash_val)  
            self.put(key, value, hash_new=hash_val, first=False)

    def get(self, key):
        """ Метод для получения значения по ключю
        Если ключа нет, возбуждает исключение ValueError

        >>> table = HashTable(11)
        >>> table['cat'] = 'Hash is 3'
        >>> table.values
        [None, None, None, 'Hash is 3', None, None, None, None, None, None, None]
        >>> table[555]
        Traceback (most recent call last):
        ...
        ValueError: Key 555 does not exist
        """
        hash_val = self.__hash_function(key)
        if self.__keys[hash_val] == key:
            return self.__values[hash_val]
        else:
            start_hash = hash_val
            new_hash = self.__rehash(hash_val)
            while (self.__keys[new_hash] is not None and
                   self.__keys[new_hash] != key and
                   start_hash != new_hash):
                new_hash = self.__rehash(new_hash)
            if self.__keys[new_hash] == key:
                return self.__values[new_hash]
            else:
                raise ValueError(f'Key {key} does not exist')

    def remove(self, key):
        """ Метод для удаления элемента по ключю
        Если данного ключа нет, позбуждает исключение ValueError
        Если таблица пуста, возбуждает исключение EmptyTable
        >>> table = HashTable(11)
        >>> del table[123]
        Traceback (most recent call last):
        ...
        EmptyTable: Table is empty
        >>> table['start'] = 194
        >>> table[123] = 'value'
        >>> table['house'] = 'white'
        >>> table.values
        [None, None, 194, 'value', 'white', None, None, None, None, None, None]
        >>> del table['start']
        >>> table.values
        [None, None, '!#!#!', 'value', 'white', None, None, None, None, None, None]
        >>> del table[666]
        Traceback (most recent call last):
        ...
        ValueError: Key 666 does not exist
        """
        hash_val = self.__hash_function(key)
        if self.__fill == 0:
            raise EmptyTable('Table is empty')
        if self.__keys[hash_val] == key:
            self.__values[hash_val] = '!#!#!'
            self.__keys[hash_val] = '!#!#!'
            self.__fill -= 1
        else:
            new_hash = self.__rehash(hash_val)
            while (self.__keys[new_hash] is not None and
                   self.__keys[new_hash] != key and
                   start_hash != new_hash):
                new_hash = self.__rehash(new_hash)
            if self.__keys[new_hash] == key:
                self.__values[new_hash] = '!#!#!'
                self.__keys[new_hash] = '!#!#!'
                self.__fill -= 1
            else:
                raise ValueError(f'Key {key} does not exist')


if __name__ == '__main__':
    import doctest
    import time
    import random
    doctest.testmod()
    table_size = 3571 # большое простое число
    steps = 1000 # кол-во шагов для получения среднего
    time_inset_30 = [None] * steps
    time_search_30 = [None] * steps
    time_inset_100 = [None] * steps
    time_search_100 = [None] * steps
    # при заполнении на 30%
    for k in range(steps):
        keys = [random.choice(range(50)) for x in range(table_size//3)]
        table = HashTable(table_size)
        start_time = time.process_time()
        for key in keys:
            table[key] = key
        time_inset_30[k] = time.process_time() - start_time
        # print('Время вставки при заполнении 30%: {0:.6f}'.format(time.process_time() - start_time))
        start_time = time.process_time()
        random.shuffle(keys)
        for key in keys:
            tmp = table[key]
        time_search_30[k] = time.process_time() - start_time
        # print('Время поиска при заполнении 30%: {0:.6f}'.format(time.process_time() - start_time))
    # при заполнении на 100%
    for k in range(steps):
        keys = [random.choice(range(50)) for x in range(table_size)]
        table = HashTable(table_size)
        start_time = time.process_time()
        for key in keys:
            table[key] = key
        time_inset_100[k] = time.process_time() - start_time
        # print('Время вставки при заполнении 100%: {0:.6f}'.format(time.process_time() - start_time))
        start_time = time.process_time()
        random.shuffle(keys)
        for key in keys:
            tmp = table[key]
        time_search_100[k] = time.process_time() - start_time
        # print('Время поиска при заполнении 100%: {0:.6f}'.format(time.process_time() - start_time))
    print('При заполнении таблицы на 30%: ')
    print('\tСреднее время вставки: {0:.6f} секунд'.format(sum(time_inset_30) / steps))
    print('\tСреднее время поиска: {0:.6f} секунд'.format(sum(time_search_30) / steps))
    print('При заполнении  таблицы на 100%: ')
    print('\tСреднее время вставки: {0:.6f} секунд'.format(sum(time_inset_100) / steps))
    print('\tСреднее время поиска: {0:.6f} секунд'.format(sum(time_search_100) / steps))

    """ 
    --------- Результаты теста скорости вставки и поиска при 1000 проверок ---------
    При заполнении таблицы на 30%: 
        Среднее время вставки: 0.001094 секунд
        Среднее время поиска: 0.001516 секунд
    При заполнении  таблицы на 100%: 
        Среднее время вставки: 0.003484 секунд
        Среднее время поиска: 0.004375 секунд
    """