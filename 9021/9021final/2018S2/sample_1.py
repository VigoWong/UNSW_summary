
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
    w = ''
    if not word:
        print('\'\'')
    else:
        for i in range(len(word)):
            if not w:
                w+=word[i]
                continue
            if word[i] != w[-1]:
                w+=word[i]
            else:
                continue
        print(f'\'{w}\'')
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()

