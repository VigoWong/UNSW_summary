from collections import defaultdict
def f(N):
    '''
    >>> f(20)
    Here are your banknotes:
    $20: 1
    >>> f(40)
    Here are your banknotes:
    $20: 2
    >>> f(42)
    Here are your banknotes:
    $2: 1
    $20: 2
    >>> f(43)
    Here are your banknotes:
    $1: 1
    $2: 1
    $20: 2
    >>> f(45)
    Here are your banknotes:
    $5: 1
    $20: 2
    >>> f(2537)
    Here are your banknotes:
    $2: 1
    $5: 1
    $10: 1
    $20: 1
    $100: 25
    '''
    dic = {100:0, 20:0, 10:0, 5:0, 2:0, 1:0}
    for k in dic.keys():
        if N // k != 0:
            dic[k] += (N // k)
            N %= k
    print('Here are your banknotes:')
    keys = list(dic.keys())
    keys = reversed(keys)
    for k in keys:
        if dic[k] != 0:
            print(f'${k}: {dic[k]}')
            
            
    
    
    
    


if __name__ == '__main__':
    import doctest
    doctest.testmod()
