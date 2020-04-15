
dictionary_file = 'dictionary.txt'

def number_of_words_in_dictionary(word_1, word_2):
    '''
    "dictionary.txt" is stored in the working directory.

    >>> number_of_words_in_dictionary('company', 'company')
    Could not find company in dictionary.
    >>> number_of_words_in_dictionary('company', 'comparison')
    Could not find at least one of company and comparison in dictionary.
    >>> number_of_words_in_dictionary('COMPANY', 'comparison')
    Could not find at least one of COMPANY and comparison in dictionary.
    >>> number_of_words_in_dictionary('company', 'COMPARISON')
    Could not find at least one of company and COMPARISON in dictionary.
    >>> number_of_words_in_dictionary('COMPANY', 'COMPANY')
    COMPANY is in dictionary.
    >>> number_of_words_in_dictionary('COMPARISON', 'COMPARISON')
    COMPARISON is in dictionary.
    >>> number_of_words_in_dictionary('COMPANY', 'COMPARISON')
    Found 14 words between COMPANY and COMPARISON in dictionary.
    >>> number_of_words_in_dictionary('COMPARISON', 'COMPANY')
    Found 14 words between COMPARISON and COMPANY in dictionary.
    >>> number_of_words_in_dictionary('CONSCIOUS', 'CONSCIOUSLY')
    Found 2 words between CONSCIOUS and CONSCIOUSLY in dictionary.
    >>> number_of_words_in_dictionary('CONSCIOUS', 'CONSCIENTIOUS')
    Found 3 words between CONSCIOUS and CONSCIENTIOUS in dictionary.
    '''
    with open('dictionary.txt', 'r') as f:
        ls = [''.join(l.strip().split()) for l in f.readlines()]
        s = set(ls)
    if word_1 == word_2:
        if word_1 not in s:
            print(f'Could not find {word_1} in dictionary.')
        else:
            print(f'{word_1} is in dictionary.')
    else:
        if word_1 in s and word_2 in s:
            a = ls.index(word_1)
            b = ls.index(word_2)
            print(f'Found {abs(a-b)+1} words between {word_1} and {word_2} in dictionary.')
        else:
            print(f'Could not find at least one of {word_1} and {word_2} in dictionary.')
    # REPLACE THE PREVIOUS LINE WITH YOUR CODE

               
if __name__ == '__main__':     
    import doctest
    doctest.testmod()
