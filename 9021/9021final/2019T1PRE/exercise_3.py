from math import sqrt
import operator
from itertools import compress
from collections import defaultdict


def p(n):
    sie = bytearray([True]) * (n//2)
    for i in range(3, int(n**0.5)+1, 2):
        if sie[i//2]:
            sie[i*i//2::i] = bytearray((n-i*i-1)//(2*i)+1)
    return [2, *compress(range(3, n, 2), sie[1::])]
    
    

def single_factors(number):
    '''
    Returns the product of the prime divisors of "number"
    (using each prime divisor only once).

    You can assume that "number" is an integer at least equal to 2.

    >>> single_factors(2)
    2
    >>> single_factors(4096)                 # 4096 == 2**12
    2
    >>> single_factors(85)                   # 85 == 5 * 17
    85
    >>> single_factors(10440125)             # 10440125 == 5**3 * 17**4
    85
    >>> single_factors(154)                  # 154 == 2 * 7 * 11
    154
    >>> single_factors(52399401037149926144) # 52399401037149926144 == 2**8 * 7**2 * 11**15
    154
    '''
    n = number
    p_ls = p(number+1)
    o_dict = defaultdict(int)
    for a in p_ls:
        while n % a == 0:
            o_dict[a]+=1
            n//=a
    o_ls = []
    mul = 1
    for k in o_dict.keys():
        mul*= k
    return mul
        
            
    
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
