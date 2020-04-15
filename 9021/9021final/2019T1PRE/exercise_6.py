# ord(c) returns the encoding of character c.
# chr(e) returns the character encoded by e.


def rectangle(width, height):
    '''
    Displays a rectangle by outputting lowercase letters, starting with a,
    in a "snakelike" manner, from left to right, then from right to left,
    then from left to right, then from right to left, wrapping around when z is reached.
    
    >>> rectangle(1, 1)
    a
    >>> rectangle(2, 3)
    ab
    dc
    ef
    >>> rectangle(3, 2)
    abc
    fed
    >>> rectangle(17, 4)
    abcdefghijklmnopq
    hgfedcbazyxwvutsr
    ijklmnopqrstuvwxy
    ponmlkjihgfedcbaz
    '''
    a_a = ord('a')
    cur = 0
    for h in range(height):
        if h %2 == 0:
            for w in range(1, width+1):
                print(chr(a_a+(cur + w-1)%26), end = '')
            print()
            cur += width
        else:
            for w in range(width, 0, -1):
                print(chr(a_a+(cur + w-1)%26), end = '')
            print()
            cur += width
            

if __name__ == '__main__':
    import doctest
    doctest.testmod()
