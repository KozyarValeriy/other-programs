""" Функция для проверки, является ли дерево бинарным деревом

>>> import BinaryTree
>>> tree = BinaryTree.BinaryTree()
>>> tree.insert(125)
>>> tree.insert(7)
>>> tree.insert(252)
>>> tree.insert(1)
>>> tree.insert(60)
>>> tree.insert(10)
>>> tree.insert(30)
>>> tree.insert(2)
>>> answer = is_binary_tree(tree.root, 'left_child', 'right_child', 'value')
>>> answer
True
>>> tree.rebalance()
>>> answer = is_binary_tree(tree.root, 'left_child', 'right_child', 'value')
>>> answer
True
>>> tree.root.left_child.value = 50
>>> answer = is_binary_tree(tree.root, 'left_child', 'right_child', 'value')
>>> answer
False
"""


def lt(value_1, value_2):
    return value_1 < value_2


def gt(value_1, value_2):
    return value_1 > value_2


def check_branch(value, node, func, left: str, right: str, data: str) -> bool:
    """ Функция для проверки, являются ли все дочерние элементы
    в ветке меньше/больше головного
    
    входные параметры:
    value - значение, с которым надо сравнивать всю ветвь;
    node - узел или корень дерева для проверки;
    func - функция для сравнения значений между собой;
    left - строка с названием метода для получения левой ветви из узла;
    right - строка с названием метода для получения правой ветви из узла;
    data - строка с названием метода для получения значения из текущего узла.
    """
    if node is None:
        return True
    if func(value, getattr(node, data)):
        return check_branch(value, getattr(node, left), func, left, right, data) and \
               check_branch(value, getattr(node, right), func, left, right, data)
    else:
        return False


def is_binary_tree(node, left: str, right: str, data: str) -> bool:
    """ Функция для проверки, является ли дерево бинарным деревом

    Входные параметры:
    node - узел или корень дерева для проверки;
    left - строка с названием метода для получения левой ветви из узла;
    right - строка с названием метода для получения правой ветви из узла;
    data - строка с названием метода для получения значения из текущего узла.
    """
    if node is None:
        return True
    if check_branch(getattr(node, data), getattr(node, left), gt, left, right, data) and \
            check_branch(getattr(node, data), getattr(node, right), lt, left, right, data):
        return is_binary_tree(getattr(node, left), left, right, data) and \
               is_binary_tree(getattr(node, right), left, right, data)
    else:
        return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()
