''' Реализация структуры связный список.

>>> new_list = LinkedList()
>>> new_list.IsEmpty()
True
>>> new_list.InsertAtEnd(55)
>>> new_list.InsertAtEnd(66)
>>> new_list.InsertAtEnd('end')
>>> new_list.InsertAtHead('start')
>>> new_list.InsertAtHead('start3')
>>> new_list.DeleteAtHead()
>>> new_list.IsEmpty()
False
>>> list(new_list)
['start', 55, 66, 'end']
>>> print(new_list)
['start', 55, 66, 'end']
>>> new_list.Search('end')
True
>>> new_list.Search('anf')
False
>>> new_list.Delete(66)
>>> print(new_list)
['start', 55, 'end']
>>> new_list.Delete('start')
>>> new_list.Delete(55)
>>> new_list.Delete('end')
>>> new_list.IsEmpty()
True
'''


class Node:
    ''' Узел для Связного списка.'''

    def __init__(self, value=None, next=None):
        ''' Конструктор узла '''
        self.value = value
        self.next = next

    def get_data(self):
        ''' Метод для получения значения текущего узла '''
        return self.value

    def get_next(self):
        ''' Метод для получения следующего узла '''
        return self.next

    def set_data(self, new_data):
        ''' Метод установки значения текущего узла '''
        self.value = new_data

    def set_next(self, new_next):
        ''' Метод для установки ссылка на следующий узел '''
        self.next = new_next


class LinkedList:

    def __init__(self):
        self.head = None

    def __str__(self): 
        ''' Метод преобразования списка в строку

        >>> new_list = LinkedList()
        >>> new_list.InsertAtHead('start')
        >>> str(new_list)
        "['start']"
        '''
        if self.IsEmpty():
            return None
        result = list(self)
        return str(result)

        #result = []
        #tmp = self.head
        #result.append(tmp.get_data())  
        #while tmp.get_next():
        #    tmp = tmp.get_next()
        #    result.append(tmp.get_data())  
        #return str(result)

    def __iter__(self):
        ''' Метод для создания итератора из списка

        >>> new_list = LinkedList()
        >>> new_list.InsertAtHead('start')
        >>> new_list.InsertAtHead('new_start')
        >>> list(new_list)
        ['new_start', 'start']
        '''
        tmp = self.head
        while tmp is not None:
            yield tmp.get_data()
            tmp = tmp.get_next()

    def InsertAtEnd(self, value):
        ''' Метод для добавления элемента в конец '''
        if self.IsEmpty():
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

    def InsertAtHead(self, value):
        ''' Метод для добавления элемента в начало '''
        tmp = Node(value)
        tmp.set_next(self.head)
        self.head = tmp

    def IsEmpty(self):
        ''' Метод для проверки, пуст ли список
        >>> new_list = LinkedList()
        >>> new_list.IsEmpty()
        True
        '''
        return self.head is None
    

    def Delete(self, value):
        ''' Метод для удаления указанного элемента 
        >>> new_list = LinkedList()
        >>> new_list.InsertAtEnd(66)
        >>> new_list.InsertAtEnd('end')
        >>> new_list.InsertAtHead('start')
        >>> print(new_list)
        ['start', 66, 'end']
        >>> new_list.Delete(66)
        >>> print(new_list)
        ['start', 'end']
        >>> new_list.Delete(959)
        Traceback (most recent call last):
        ...
        IndexError: Нет такого элемента
        '''
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
        ''' Метод для удаления элемента из начала '''
        if self.IsEmpty():
            return None
        self.head = self.head.get_next() 

    def Search(self, value):
        ''' Метод для поиска элемента в списке'''
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
