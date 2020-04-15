import sys
from math import sqrt
from itertools import compress


def p(n):
    sie = bytearray([True])*(n//2)
    for i in range(3, int(n**0.5)+1 ,2):
        if sie[i//2]:
            sie[i*i//2::i] = bytearray((n-i*i-1)//(i*2)+1)
    return [2, *compress(range(3, n , 2), sie[1::])]



def f(a, b):
    '''
    Won't be tested for b greater than 10_000_000
    
    >>> f(3, 3)
    The number of prime numbers between 3 and 3 included is 1
    >>> f(4, 4)
    The number of prime numbers between 4 and 4 included is 0
    >>> f(2, 5)
    The number of prime numbers between 2 and 5 included is 3
    >>> f(2, 10)
    The number of prime numbers between 2 and 10 included is 4
    >>> f(2, 11)
    The number of prime numbers between 2 and 11 included is 5
    >>> f(1234, 567890)
    The number of prime numbers between 1234 and 567890 included is 46457
    >>> f(89, 5678901)
    The number of prime numbers between 89 and 5678901 included is 392201
    >>> f(89, 5678901)
    The number of prime numbers between 89 and 5678901 included is 392201
    '''
    if a == 2:
        ls_1 = []
        if b == 2:
            ls_2 = [2]
        else:
            ls_2 = p(b+1)
    else:
        ls_1 = p(a)
        ls_2 = p(b+1)
    out = len(set(ls_2) - set(ls_1))
    print(f'The number of prime numbers between {a} and {b} included is {out}')
    
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
