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
    s = a_a
    cur = 0
    for h in range(height):
        if h % 2 == 0:
            ls = [chr(s+(i+cur)%26) for i in range(0, width)]
        else:
            ls = [chr(s+(i+cur-1)%26) for i in range(width, 0, -1)]
        cur += width
        out = ''.join(ls)
        print(out)
        

    
    # REPLACE THE PREVIOUS LINE WITH YOUR CODE
    


if __name__ == '__main__':
    import doctest
    doctest.testmod()
