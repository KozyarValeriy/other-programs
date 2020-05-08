"""
--------- Задание ---------
Реализация очереди с приоритетом. Варианты реализации: список списков,
массив списков.
Методы к реализации:
печать очереди;
enqueue(item, priority) - поместить элемент в очередь;
dequeue() - выбрать элемент из очереди
--------- Описание и тесты ---------
Реализация очереди с приоритетом.
Реализованы методы удаления, добавления элемента по приоритету 
и проверки на наличие элементов в очереди.
ПРи вызове метода удаления, сначала удаляются элементы
с более высоким приоритетом.

>>> order = OrderWithPriority(4)
>>> order.enqueue('first', 1)
>>> order.enqueue('second', 2)
>>> order.enqueue('third', 3)
>>> order.enqueue('fourth', 2)
>>> order.enqueue('fifth', 4)
>>> print(order)
Priority: |     1|     2|     3|     4|
--------------------------------------|
    1     | first|second| third| fifth|
    2     |  None|fourth|  None|  None|
>>> order.dequeue()
'first'
>>> order.dequeue()
'second'
>>> order.dequeue()
'fourth'
>>> order.dequeue()
'third'
>>> order.dequeue()
'fifth'
>>> print(order)
Priority: |     1|     2|     3|     4|
--------------------------------------|
"""


class InvalidPriorityLevel(Exception):
    # Исключение при неправильном приоритете
    pass


class OrderWithPriority:

    def __init__(self, max_priority_level: int = 10):
        """ Constructor 
        >>> order = OrderWithPriority(4)
        >>> order.is_empty()
        True
        >>> order.max_priority_level
        4
        """
        self.__max_len_str = 4
        self.max_priority_level = max_priority_level
        self.__order = list([] for _ in range(max_priority_level))  # [None] * max_priority_level

    def __str__(self):
        """ Метод для вывода на печать очереди """
        body = ''
        pattern = '{0: ^10}'
        for i in range(2, len(self.__order) + 2):
            pattern += '|{' + str(i) + ': >{1}}'
        pattern += '|\n'
        head = pattern.format('Priority: ', self.__max_len_str, *range(1, len(self.__order) + 1))
        body += head
        body += '{0:-^{1}s}|\n'.format('-', len(head) - 2)
        step = 0
        while True:
            line = []
            for level in self.__order:
                if not level or len(level) <= step:
                    line.append("None")
                else:
                    line.append(level[step])
            if all(el == "None" for el in line):
                break
            step += 1
            body += pattern.format(step, self.__max_len_str, *line)
        return body.rstrip()

    def enqueue(self, item, priority: int):
        """ Метод для добавления элемента в очередь

        >>> order = OrderWithPriority(4)
        >>> order.enqueue(5, 1)
        >>> print(order)
        Priority: |    1|    2|    3|    4|
        ----------------------------------|
            1     |    5| None| None| None|
        >>> order.enqueue(5, 10)
        Traceback (most recent call last):
        ...
        InvalidPriorityLevel: Invalid priority level. Must be in [1..4]
        """
        if not (0 < priority <= self.max_priority_level):
            raise InvalidPriorityLevel('Invalid priority level. '
                                       f'Must be in [1..{self.max_priority_level}]')
        self.__max_len_str = len(str(item)) + 1
        if self.__max_len_str > 50:
            self.__max_len_str = 50
        elif self.__max_len_str < 5:
            self.__max_len_str = 5
        if not self.__order[priority - 1]:
            self.__order[priority - 1] = [item]
        else:
            self.__order[priority - 1].append(item)

    def dequeue(self):
        """ Метод удаления элемента из очереди 

        >>> order = OrderWithPriority(4)
        >>> order.enqueue(5, 1)
        >>> order.enqueue(8, 3)
        >>> print(order)
        Priority: |    1|    2|    3|    4|
        ----------------------------------|
            1     |    5| None|    8| None|
        >>> order.dequeue()
        5
        >>> order.dequeue()
        8
        >>> order.dequeue()
        """
        item = None
        for level in range(self.max_priority_level):
            if not self.__order[level]:
                continue
            item = self.__order[level][0]
            self.__order[level].remove(item)
            # item = self.__order[level].pop()
            if len(self.__order[level]) == 0: 
                self.__order[level] = []
            break
        return item

    def is_empty(self):
        """ Метод проверки на наличие каих то элементов в очереди 

        >>> order = OrderWithPriority(4)
        >>> order.is_empty()
        True
        >>> order.enqueue(5, 1)
        >>> order.is_empty()
        False
        """
        return all(bool(level) is False for level in self.__order)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
