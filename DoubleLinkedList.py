""" 
--------- Задание ---------
Реализовать двусвязный список (описание операций в слайдах)

--------- Описание и тесты ---------
Реализация структуры связный список.

>>> new_list = DoubleLinkedList()
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
>>> print(new_list)
['start', 55, 66, 'end']
>>> new_list.search('end')
True
>>> mid = new_list.head.get_next()
>>> mid.get_previous().value, mid.value, mid.get_next().value 
('start', 55, 66)
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


class NodeDouble:
    """ Узел для двухсвязного списка """

    def __init__(self, value=None, prev=None, next_=None):
        """ Конструктор узла """
        self.value = value
        self.prev = prev
        self.next = next_

    def get_data(self):
        """ Метод для получения значения текущего узла """
        return self.value

    def get_next(self):
        """ Метод для получения следующего узла """
        return self.next

    def get_previous(self):
        """ Метод для получения предыдущего узла """
        return self.prev
        
    def set_data(self, new_data):
        """ Метод установки значения текущего узла """
        self.value = new_data

    def set_next(self, new_next):
        """ Метод для установки ссылка на следующий узел """
        self.next = new_next

    def set_previous(self, new_prev):
        """ Метод для установки ссылка на предыдущий узел """
        self.prev = new_prev

        
class DoubleLinkedList:

    def __init__(self):
        self.head = None

    def __str__(self):
        """ Метод преобразования списка в строку
        >>> new_list = DoubleLinkedList()
        >>> new_list.insert_at_head('start')
        >>> str(new_list)
        "['start']"
        """
        if self.is_empty():
            return None
        result = []
        tmp = self.head
        result.append(tmp.get_data())  
        while tmp.get_next():
            tmp = tmp.get_next()
            result.append(tmp.get_data())  
        return str(result)

    def insert_at_end(self, value):
        """ Метод для добавления элемента в конец """
        if self.is_empty():
            self.head = NodeDouble(value)
        else:
            tmp = self.head    
            while tmp.get_next():
                tmp = tmp.get_next()
                if tmp.get_next() is None:
                    break
            tmp.set_next(NodeDouble(value))
            tmp.get_next().set_previous(tmp)

    def insert_at_head(self, value):
        """ Метод для добавления элемента в начало """
        tmp = NodeDouble(value)
        tmp.set_next(self.head)
        if not self.is_empty():
            self.head.set_previous(tmp)
        self.head = tmp

    def is_empty(self):
        """ Метод для проверки, пуст ли список
        >>> new_list = DoubleLinkedList()
        >>> new_list.is_empty()
        True
        """
        return self.head is None

    def delete(self, value):
        f""" Метод для удаления указанного элемента 
        >>> new_list = DoubleLinkedList()
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
        IndexError: Элемента {value} нет в списке
        """
        curr = self.head
        found = False
        while curr and not found:
            if curr.get_data() == value:
                found = True
            else:
                curr = curr.get_next()
        if found and curr == self.head:
            self.head = curr.get_next()
        elif found:
            curr.get_previous().set_next(curr.get_next())
        else:
            raise IndexError(f'Элемента {value} нет в списке')

    def delete_at_head(self):
        """ Метод для удаления элемента из начала """
        if self.is_empty():
            return None
        self.head = self.head.get_next() 

    def search(self, value):
        """ Метод для поиска элемента в списке """
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
