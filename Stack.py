""" 
Реализация структуры данных Стек

Реализованны методы:
push(item) - добавление элемента,
pop() 	   - удаляет и возвращает верхний элемент,
is_empty() - возвращает True, если стек пуст,
top()      - возвращает верхний элемент без удаления,
size() 	   - возвращает размер стека

>>> stack = Stack()
>>> stack.is_empty()
True
>>> stack.push(1)
>>> stack.push(2)
>>> stack.push(3)
>>> stack.push(4)
>>> stack.push(5)
>>> stack.is_empty()
False
>>> stack.items
[1, 2, 3, 4, 5]
>>> stack.pop()
5
>>> stack.top()
4
>>> stack.items
[1, 2, 3, 4]
>>> stack.size()
4
"""


class Stack:
    def __init__(self):
        self.__items = []

    @property 
    def items(self):
        return self.__items.copy()

    def is_empty(self):
        return not bool(self.__items)

    def push(self, item):
        self.__items.append(item)

    def pop(self):
        return self.__items.pop()

    def top(self):
        return self.__items[-1]

    def size(self):
        return len(self.__items)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
