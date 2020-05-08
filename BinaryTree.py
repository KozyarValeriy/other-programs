"""
Реализация бинарного дерева. Операции: вставка, поиск, печать дерева 

--------- Описание и тесты ---------
Реализация структцра Бинарного дерева.
Реализованы методы:
insert(item) - вставка элемента
search(item) - поиск элемента

>>> tree = BinaryTree()
>>> tree.insert(125)
>>> tree.insert(7)
>>> tree.insert(252)
>>> tree.insert(1)
>>> tree.insert(60)
>>> tree.insert(10)
>>> tree.insert(30)
>>> tree.insert(2)
>>> tree.search(60)
True
>>> 999 in tree
False
>>> tree.root.value
125
>>> print(tree)
[125]
[7, 252]
[1, 60, None, None]
[None, 2, 10, None, None, None, None, None]
[None, None, None, None, None, 30, None, None, None, None, None, None, None, None, None, None]
>>> tree.rebalance()
>>> tree.root.value
30
>>> tree.rebalance()
>>> print(tree)
[30]
[7, 125]
[2, 10, 60, 252]
[1, None, None, None, None, None, None, None]
"""


class TreeNode:
    """ Класс элемента узла у дерева """

    def __init__(self, value, left=None, right=None, parent=None):
        self.value = value
        self.left_child = left
        self.right_child = right
        self.parent = parent

    def is_lean(self):
        """ Метод для опредления, является ли узел листом
        Возвращает True если узел является листом, иначе False.
        """
        return not (self.right_child or self.left_child)


class BinaryTree:
    """ Класс бинарнго дерева """

    def __init__(self):
        self.root = None
        self.size = 0
        
    def __str__(self):
        result = []
        tmp = []
        # если узел не пустой
        if self.root is not None:
            result.append([self.root.value])
        # если пустой, вернуть пустую строку
        else:
            return ''
        tmp.append(self.root.left_child)
        tmp.append(self.root.right_child)
        # делать, пока есть левый или правый потомок
        while not all(el is None for el in tmp):
            tmp_next = []
            tmp_result = []
            for current_node in tmp:
                if current_node is None: 
                    tmp_result.append(None)
                    for _ in range(2):
                        tmp_next.append(None)
                    continue
                tmp_result.append(current_node.value)
                tmp_next.append(current_node.left_child)
                tmp_next.append(current_node.right_child)
            result.append(tmp_result)
            tmp = tmp_next
        return '\n'.join([str(level) for level in result])
        
    def __len__(self):
        """ Магический метод для поддержки len() """
        return self.size

    def __contains__(self, item):
        """ Магический методя для поддержки оператора in 
        
        >>> tree = BinaryTree()
        >>> tree.insert(125)
        >>> tree.insert(7)
        >>> 125 in tree
        True
        >>> 999 in tree
        False
        """
        return self.search(item)    

    def __iter__(self):
        """ Магический метод для поддеожки протокола итерации. 
        Итерация происходит в по схеме обхода в глубину. 

        >>> tree = BinaryTree()
        >>> tree.insert(125)
        >>> tree.insert(7)
        >>> tree.insert(252)
        >>> list(tree)
        [125, 7, 252]
        """
        return self.__iter(self.root)
 
    def __iter(self, current_node):
        if current_node is not None:
            yield current_node.value
            if not current_node.is_lean():
                for el in self.__iter(current_node.left_child):
                    yield el
                for el in self.__iter(current_node.right_child):
                    yield el

    def insert(self, item):
        """ Метод для вставки элемента в дерево 

        >>> tree = BinaryTree()
        >>> tree.insert(125)
        >>> tree.insert(7)
        >>> tree.search(125), tree.search(7), tree.search(99)
        (True, True, False)
        """
        if self.root is not None:
            if item in self:
                return
            self.__insert(item, self.root)
            # self.type = type(item)
        else:
            self.root = TreeNode(item)
        self.size += 1

    def __insert(self, item, current_node): 
        """ Рекурсивный метод для вставки элемента.
        Ищет подходящее мето для элемента и создает новый лист с его значением.
        """
        if item < current_node.value:
            if current_node.left_child:
                self.__insert(item, current_node.left_child)
            else:
                current_node.left_child = TreeNode(item, parent=current_node)
        else:
            if current_node.right_child:
                self.__insert(item, current_node.right_child)
            else:
                current_node.right_child = TreeNode(item, parent=current_node)

    def search(self, item):
        """ Метод для поиска элемента в дереве 

        >>> tree = BinaryTree()
        >>> tree.insert(125)
        >>> tree.insert(7)
        >>> tree.search(125), tree.search(7), tree.search(99)
        (True, True, False)
        """
        return self.__search(item, self.root)

    def __search(self, item, current_node): 
        """ Рекурсивная функция для поиска значения в дереве.
        Проходит до листа. Если находи элемент, то возвращает True.
        При достижении листа возвращает False.
        """
        if current_node is None:
            return False
        if item < current_node.value:
            return self.__search(item, current_node=current_node.left_child)
        elif item > current_node.value:
            return self.__search(item, current_node=current_node.right_child)
        else:
            return True

    def rebalance(self):
        """ Метод для создание сбалансированного дерева из текущего 

        >>> tree = BinaryTree()
        >>> tree.insert(125)
        >>> tree.insert(50)
        >>> tree.insert(20)
        >>> tree.root.value, tree.root.left_child.value, tree.root.right_child
        (125, 50, None)
        >>> tree.root.value, tree.root.left_child.value, tree.root.right_child
        (125, 50, None)
        >>> tree.rebalance()
        >>> tree.root.value
        50
        >>> tree.root.left_child.value, tree.root.right_child.value
        (20, 125)
        """
        all_tree = list(self)
        all_tree.sort()
        self.root = None
        self.size = 0
        self.__rebalance(all_tree)

    def __rebalance(self, branch):
        """ Рекурсивный метод для балансировки дерева
        На вход подается отсортированный список, который делится пополам.
        Средний элемент записываться как узел. Далее метод вызывается
        для левой и правой части входного списка относительно середины.
        """
        m = len(branch)
        branch_left = branch[:m//2]
        branch_right = branch[(m//2) + 1:]
        self.insert(branch[m//2])
        if branch_left:
            self.__rebalance(branch_left)
        if branch_right:
            self.__rebalance(branch_right)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
