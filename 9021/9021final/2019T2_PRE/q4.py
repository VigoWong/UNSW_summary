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
    if not word:
        return ''
    else:
        
        ls = []
        for i in word:
            if not ls:
                ls.append([i])
            else:
                if ord(ls[-1][-1])+1 == ord(i):
                    ls[-1].append(i)
                else:
                    ls.append([i])
        len_ls = [len(a) for a in ls]
        desired_length = max(len_ls)
        index = len_ls.index(desired_length)
        desired_substring = ''.join(ls[index])
        return desired_substring
    # REPLACE THE PREVIOUS LINE WITH YOUR CODE                


if __name__ == '__main__':
    import doctest
    doctest.testmod()
