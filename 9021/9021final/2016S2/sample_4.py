from numpy import array

def is_heterosquare(square):
    '''
    A heterosquare of order n is an arrangement of the integers 1 to n**2 in a square,
    such that the rows, columns, and diagonals all sum to DIFFERENT values.
    In contrast, magic squares have all these sums equal.
    
    
    >>> is_heterosquare([[1, 2, 3],\
                         [8, 9, 4],\
                         [7, 6, 5]])
    True
    >>> is_heterosquare([[1, 2, 3],\
                         [9, 8, 4],\
                         [7, 6, 5]])
    False
    >>> is_heterosquare([[2, 1, 3, 4],\
                         [5, 6, 7, 8],\
                         [9, 10, 11, 12],\
                         [13, 14, 15, 16]])
    True
    >>> is_heterosquare([[1, 2, 3, 4],\
                         [5, 6, 7, 8],\
                         [9, 10, 11, 12],\
                         [13, 14, 15, 16]])
    False
    '''
    n = len(square)
    if any(len(line) != n for line in square):
        return False
    # Insert your code here
    s = array(square)
    row_sum = [sum(l.tolist()) for l in s]
    colmn_sum = [sum(l.tolist()) for l in s.T]
    dia_1 = sum([square[i][i] for i in range(len(square))])
    dia_2 = sum([square[-i][-i] for i in range(1, 1+len(square))])
    k = set(row_sum) | set(colmn_sum)
    k.add(dia_1)
    k.add(dia_2)
    if len(row_sum)+len(colmn_sum)+2 == len(k):
        return True
    else:
        return False

# Possibly define other functions

    
if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    is_heterosquare([[1, 2, 3, 4], \
                     [5, 6, 7, 8], \
                     [9, 10, 11, 12], \
                     [13, 14, 15, 16]])
