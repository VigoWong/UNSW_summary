class Node:
    def __init__(self, value = None):
        self.value = value
        self.next_node = None
        self.previous_node = None


class DoublyLinkedList:
    def __init__(self, L = None):
        '''Creates an empty list or a list built from a subscriptable object.

        >>> DoublyLinkedList().print_from_head_to_tail()
        >>> DoublyLinkedList().print_from_tail_to_head()
        >>> DoublyLinkedList([]).print_from_head_to_tail()
        >>> DoublyLinkedList([]).print_from_tail_to_head()
        >>> DoublyLinkedList((0,)).print_from_head_to_tail()
        0
        >>> DoublyLinkedList((0,)).print_from_tail_to_head()
        0
        >>> DoublyLinkedList(range(4)).print_from_head_to_tail()
        0, 1, 2, 3
        >>> DoublyLinkedList(range(4)).print_from_tail_to_head()
        3, 2, 1, 0
        '''
        

    def print_from_head_to_tail(self):
        '''
        >>> DoublyLinkedList().print_from_head_to_tail()
        >>> DoublyLinkedList(range(1)).print_from_head_to_tail()
        0
        >>> DoublyLinkedList(range(2)).print_from_head_to_tail()
        0, 1
        >>> DoublyLinkedList(range(3)).print_from_head_to_tail()
        0, 1, 2
        '''
        

    def print_from_tail_to_head(self):
        '''
        >>> DoublyLinkedList().print_from_tail_to_head()
        >>> DoublyLinkedList(range(1)).print_from_tail_to_head()
        0
        >>> DoublyLinkedList(range(2)).print_from_tail_to_head()
        1, 0
        >>> DoublyLinkedList(range(3)).print_from_tail_to_head()
        2, 1, 0
        '''
        

    def keep_every_second_element(self):
        '''
        >>> L = DoublyLinkedList(); L.keep_every_second_element()
        >>> L.print_from_head_to_tail()
        >>> L.print_from_tail_to_head()
        >>> L = DoublyLinkedList([1]); L.keep_every_second_element()
        >>> L.print_from_head_to_tail()
        1
        >>> L.print_from_tail_to_head()
        1
        >>> L = DoublyLinkedList([1, 2]); L.keep_every_second_element()
        >>> L.print_from_head_to_tail()
        1
        >>> L.print_from_tail_to_head()
        1
        >>> L = DoublyLinkedList([1, 2, 3]); L.keep_every_second_element()
        >>> L.print_from_head_to_tail()
        1, 3
        >>> L.print_from_tail_to_head()
        3, 1
        >>> L = DoublyLinkedList([1, 2, 3, 4]); L.keep_every_second_element()
        >>> L.print_from_head_to_tail()
        1, 3
        >>> L.print_from_tail_to_head()
        3, 1
        >>> L = DoublyLinkedList([1, 2, 3, 4, 5]); L.keep_every_second_element()
        >>> L.print_from_head_to_tail()
        1, 3, 5
        >>> L.print_from_tail_to_head()
        5, 3, 1
        '''
        # Insert your code here
        


if __name__ == '__main__':
    import doctest
    doctest.testmod()
