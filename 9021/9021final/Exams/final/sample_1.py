
def remove_consecutive_duplicates(word):
    '''
    >>> remove_consecutive_duplicates('')
    ''
    >>> remove_consecutive_duplicates('a')
    'a'
    >>> remove_consecutive_duplicates('ab')
    'ab'
    >>> remove_consecutive_duplicates('aba')
    'aba'
    >>> remove_consecutive_duplicates('aaabbbbbaaa')
    'aba'
    >>> remove_consecutive_duplicates('abcaaabbbcccabc')
    'abcabcabc'
    >>> remove_consecutive_duplicates('aaabbbbbaaacaacdddd')
    'abacacd'
    '''
    # Insert your code here (the output is returned, not printed out)
    if word == '':
        print('\'\'')
    else:
        ls= ''
        for w in word:
            if not ls:
                ls += w
            else:
                if w != ls[-1]:
                    ls+=w
                else:
                    continue
        print('\''+ls+'\'')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
