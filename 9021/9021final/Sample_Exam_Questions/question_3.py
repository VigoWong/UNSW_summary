# COMP9021 19T3 - Rachid Hamadi
# Sample Exam Question 3


'''
Will be tested with n at least equal to 2, and "not too large".
'''
from itertools import compress
from collections import defaultdict
from math import sqrt



def prime(n):
    sie = bytearray([True])*(n//2)
    for i in range(3, int(n**0.5)+1,2):
        if sie[i//2]:
            sie[i*i//2::i] = bytearray((n-i*i-1)//(2*i)+1)
    return [2, *compress(range(3, n, 2), sie[1:])]
    



def f(n):
    '''
    >>> f(2)
    The decomposition of 2 into prime factors reads:
       2 = 2
    >>> f(3)
    The decomposition of 3 into prime factors reads:
       3 = 3
    >>> f(4)
    The decomposition of 4 into prime factors reads:
       4 = 2^2
    >>> f(5)
    The decomposition of 5 into prime factors reads:
       5 = 5
    >>> f(6)
    The decomposition of 6 into prime factors reads:
       6 = 2 x 3
    >>> f(8)
    The decomposition of 8 into prime factors reads:
       8 = 2^3
    >>> f(10)
    The decomposition of 10 into prime factors reads:
       10 = 2 x 5
    >>> f(15)
    The decomposition of 15 into prime factors reads:
       15 = 3 x 5
    >>> f(100)
    The decomposition of 100 into prime factors reads:
       100 = 2^2 x 5^2
    >>> f(5432)
    The decomposition of 5432 into prime factors reads:
       5432 = 2^3 x 7 x 97
    >>> f(45103)
    The decomposition of 45103 into prime factors reads:
       45103 = 23 x 37 x 53
    >>> f(45100)
    The decomposition of 45100 into prime factors reads:
       45100 = 2^2 x 5^2 x 11 x 41
    '''
    factors = {}
    # Insert your code here
    
    sq = int(sqrt(n))+1
    prime_ls = prime(sq)
    num_count = {}
    n_n = n
    for i in prime_ls:
        while n_n % i == 0:
            if i in num_count.keys():
                num_count[int(i)] +=1
            else:
                num_count[int(i)] = 1
            n_n /= i
    if n_n != 1:
        num_count[int(n_n)] = 1
    ls = []
    for i in num_count.keys():
        if num_count[i] != 1:
            ls.append(f'{i}^{num_count[i]}')
        else:
            ls.append(str(i))
    out = ' x '.join(ls)
    print(f'The decomposition of {n} into prime factors reads:')
    print(f'   {n} = {out}')
            
        
    
    
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()
