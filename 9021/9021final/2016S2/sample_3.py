import sys
from itertools import compress

def p(n):
    sie = bytearray([True])*(n//2)
    for i in range(3, int(n**0.5)+1, 2):
        if sie[i//2]:
            sie[i*i//2::i] = bytearray((n-i*i-1)//(i*2)+1)
    return [2, *compress(range(3,n,2), sie[1::])]

def f(a, b):
    '''
    The prime numbers between 2 and 12 (both included) are: 2, 3, 5, 7, 11
    The gaps between successive primes are: 0, 1, 1, 3.
    Hence the maximum gap is 3.
    
    Won't be tested for b greater than 10_000_000
    
    >>> f(3, 3)
    The maximum gap between successive prime numbers in that interval is 0
    >>> f(3, 4)
    The maximum gap between successive prime numbers in that interval is 0
    >>> f(3, 5)
    The maximum gap between successive prime numbers in that interval is 1
    >>> f(2, 12)
    The maximum gap between successive prime numbers in that interval is 3
    >>> f(5, 23)
    The maximum gap between successive prime numbers in that interval is 3
    >>> f(20, 106)
    The maximum gap between successive prime numbers in that interval is 7
    >>> f(31, 291)
    The maximum gap between successive prime numbers in that interval is 13
    '''
    if a <= 0 or b < a:
        sys.exit()
    max_gap = 0
    a_ls = p(a)
    b_ls = p(b+1)
    gap = 0
    ls = sorted(list(set(b_ls) - set(a_ls)))
    for i in range(1, len(ls)):
        cur = ls[i] - ls[i-1]-1
        if cur>gap:
            gap = cur
    print(f'The maximum gap between successive prime numbers in that interval is {gap}')
        
    # Insert your code here


if __name__ == '__main__':
    import doctest
    doctest.testmod()
