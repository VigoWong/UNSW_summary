
def rearrange(number):
    '''
    Returns an integer consisting of all nonzero digits in "number",
    from smallest to largest.

    You can assume that "number" is a valid strictly positive integer.
    
    >>> rearrange(1)
    1
    >>> rearrange(200)
    2
    >>> rearrange(395)
    359
    >>> rearrange(10029001)
    1129
    >>> rearrange(301302004)
    12334
    >>> rearrange(9409898038908908934890)
    33448888889999999
    '''
    # return -1
    # REPLACE THE PREVIOUS LINE WITH YOUR CODE
    a = str(number)
    b = []
    for i in a:
        if i != '0':
            b.append(i)
    if b:
        b = int(''.join(sorted(b)))
    return b
    
        
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
