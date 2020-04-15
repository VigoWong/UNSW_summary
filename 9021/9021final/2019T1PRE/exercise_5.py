# You might find the ord() function useful.

def longest_leftmost_sequence_of_consecutive_letters(word):
    '''
    You can assume that "word" is a string of
    nothing but lowercase letters.
    
    >>> longest_leftmost_sequence_of_consecutive_letters('')
    ''
    >>> longest_leftmost_sequence_of_consecutive_letters('a')
    'a'
    >>> longest_leftmost_sequence_of_consecutive_letters('zuba')
    'z'
    >>> longest_leftmost_sequence_of_consecutive_letters('ab')
    'ab'
    >>> longest_leftmost_sequence_of_consecutive_letters('bcab')
    'bc'
    >>> longest_leftmost_sequence_of_consecutive_letters('aabbccddee')
    'ab'
    >>> longest_leftmost_sequence_of_consecutive_letters('aefbxyzcrsdt')
    'xyz'
    >>> longest_leftmost_sequence_of_consecutive_letters('efghuvwijlrstuvabcde')
    'rstuv'
    '''
    # REPLACE THE PREVIOUS LINE WITH YOUR CODE
    if not word:
        return ''
    else:
        t = []
        for i in word:
            if not t:
                t.append([i])
            else:
                if ord(i) == ord(t[-1][-1])+1:
                    t[-1].append(i)
                else:
                    t.append([i])
        len_ls = []
        for i in t:
            len_ls.append(len(i))
        max_len = max(len_ls)
        index = len_ls.index(max_len)
        out = ''.join(t[index])
        return out
            
            
            
        


if __name__ == '__main__':
    import doctest
    doctest.testmod()
