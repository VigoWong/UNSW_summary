
def display(square):
    print('\n'.join(' '.join(f'{x:2d}' for x in row) for row in square))

def check_out_square_and_fix_if_corrupted(square):
    '''
    Call "good square" an n x n matrix with n >= 2 consisting of all numbers
    between 1 and n ** 2.
    Call "corrupted square" a good square exactly one of whose entries has been
    replaced by 0.

    Note: marks can be scored by just checking whether the square is good or corrupted,
    without fixing it in case it is corrupted -- but hard coding won't help.
    
    >>> check_out_square_and_fix_if_corrupted([[1, 5, 7],\
                                               [2, 9, 3],\
                                               [6, 4, 8]])
    Here is the square: 
     1  5  7
     2  9  3
     6  4  8
    It is a good square.
    >>> check_out_square_and_fix_if_corrupted([[1, 5, 7],\
                                               [2, 9, 3],\
                                               [6, 10, 8]])
    Here is the square: 
     1  5  7
     2  9  3
     6 10  8
    It is neither a good nor a corrupted square.
    >>> check_out_square_and_fix_if_corrupted([[1, 5, 7],\
                                               [2, 9, 0],\
                                               [6, 4, 8]])
    Here is the square: 
     1  5  7
     2  9  0
     6  4  8
    It is a corrupted square, the good square being:
     1  5  7
     2  9  3
     6  4  8
    >>> check_out_square_and_fix_if_corrupted([[1, 5, 7, 11],\
                                               [2, 9, 0, 16],\
                                               [6, 4, 8, 12],\
                                               [13, 14, 15, 2]])
    Here is the square: 
     1  5  7 11
     2  9  0 16
     6  4  8 12
    13 14 15  2
    It is neither a good nor a corrupted square.
    >>> check_out_square_and_fix_if_corrupted([[1, 5, 7, 11],\
                                               [3, 9, 0, 16],\
                                               [6, 4, 8, 12],\
                                               [13, 14, 15, 2]])
    Here is the square: 
     1  5  7 11
     3  9  0 16
     6  4  8 12
    13 14 15  2
    It is a corrupted square, the good square being:
     1  5  7 11
     3  9 10 16
     6  4  8 12
    13 14 15  2
    '''
    n = len(square)
    if n < 2 or any(len(line) != n for line in square):
        return False
    print('Here is the square: ')
    display(square)
    good_square = False
    corrupted_square = False
    val_ls =[]
    # Insert your code here
    for l in range(len(square)):
        for r in range(len(square[l])):
            val_ls.append(square[l][r])
    len_s= len(square)
    

    for i in range(1, len_s**2+1):
        if i not in val_ls:
            good_square = False
            break
        good_square = True

    if not good_square:
        count=0
        r, c = 0, 0
        for i in range(1, len_s**2+1):
            if i not in val_ls:
                if not count and 0 in val_ls:
                    count+=1
                    oo = val_ls.index(0)
                    r = (oo-1)//len_s
                    c = (oo) % len_s
                    val = i
                    continue
                else:
                    corrupted_square = False
                    break
            corrupted_square = True
    if corrupted_square:
        square[r][c] = val
    
    
    
    if good_square:
        print('It is a good square.')
    else:
        if not corrupted_square:
            print('It is neither a good nor a corrupted square.')
        else:
            print('It is a corrupted square, the good square being:')
            display(square)

    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
