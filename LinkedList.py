""" Реализация структуры связный список.

>>> new_list = LinkedList()
>>> new_list.is_empty()
True
>>> new_list.insert_at_end(55)
>>> new_list.insert_at_end(66)
>>> new_list.insert_at_end('end')
>>> new_list.insert_at_head('start')
>>> new_list.insert_at_head('start3')
>>> new_list.delete_at_head()
>>> new_list.is_empty()
False
>>> list(new_list)
['start', 55, 66, 'end']
>>> print(new_list)
['start', 55, 66, 'end']
>>> new_list.search('end')
True
>>> new_list.search('anf')
False
>>> new_list.delete(66)
>>> print(new_list)
['start', 55, 'end']
>>> new_list.delete('start')
>>> new_list.delete(55)
>>> new_list.delete('end')
>>> new_list.is_empty()
True
"""


class Node:
    """ Узел для Связного списка."""

    def __init__(self, value=None, next_=None):
        """ Конструктор узла """
        self.value = value
        self.next = next_

    def get_data(self):
        """ Метод для получения значения текущего узла """
        return self.value

    def get_next(self):
        """ Метод для получения следующего узла """
        return self.next

    def set_data(self, new_data):
        """ Метод установки значения текущего узла """
        self.value = new_data

    def set_next(self, new_next):
        """ Метод для установки ссылка на следующий узел """
        self.next = new_next


class LinkedList:

    def __init__(self):
        self.head = None

    def __str__(self):
        """ Метод преобразования списка в строку

        >>> new_list = LinkedList()
        >>> new_list.insert_at_head('start')
        >>> str(new_list)
        "['start']"
        """
        if self.is_empty():
            return None
        result = list(self)
        return str(result)

    def __iter__(self):
        """ Метод для создания итератора из списка

        >>> new_list = LinkedList()
        >>> new_list.insert_at_head('start')
        >>> new_list.insert_at_head('new_start')
        >>> list(new_list)
        ['new_start', 'start']
        """
        tmp = self.head
        while tmp is not None:
            yield tmp.get_data()
            tmp = tmp.get_next()

    def insert_at_end(self, value):
        """ Метод для добавления элемента в конец """
        if self.is_empty():
            self.head = Node(value)
        elif self.head.get_next() is None:
            self.head.set_next(Node(value))
            return
        else:
            tmp = self.head    
            while tmp.get_next():
                tmp = tmp.get_next()
                if tmp.get_next() is None:
                    tmp.set_next(Node(value))
                    return

    def insert_at_head(self, value):
        """ Метод для добавления элемента в начало """
        tmp = Node(value)
        tmp.set_next(self.head)
        self.head = tmp

    def is_empty(self):
        """ Метод для проверки, пуст ли список
        >>> new_list = LinkedList()
        >>> new_list.is_empty()
        True
        """
        return self.head is None

    def delete(self, value):
        """ Метод для удаления указанного элемента 
        >>> new_list = LinkedList()
        >>> new_list.insert_at_end(66)
        >>> new_list.insert_at_end('end')
        >>> new_list.insert_at_head('start')
        >>> print(new_list)
        ['start', 66, 'end']
        >>> new_list.delete(66)
        >>> print(new_list)
        ['start', 'end']
        >>> new_list.delete(959)
        Traceback (most recent call last):
        ...
        IndexError: Нет такого элемента
        """
        curr = self.head
        prev = None
        found = False
        while curr is not None and not found:
            if curr.get_data() == value:
                found = True
            else:
                prev = curr
                curr = curr.get_next()
        if found and prev is None:
            self.head = curr.get_next()
        elif found:
            prev.set_next(curr.get_next())
        else:
            raise IndexError('Нет такого элемента')

    def DeleteAtHead(self):
        """ Метод для удаления элемента из начала """
        if self.is_empty():
            return None
        self.head = self.head.get_next() 

    def Search(self, value):
        """ Метод для поиска элемента в списке"""
        tmp = self.head
        while tmp is not None:
            if tmp.get_data() == value:
                return True
            else:
                tmp = tmp.get_next()
        return False


if __name__ == "__main__":
    import doctest
    doctest.testmod()
