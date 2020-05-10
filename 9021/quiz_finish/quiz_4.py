# COMP9021 19T3 - Rachid Hamadi
# Quiz 4 *** Due Thursday Week 5
#
# Prompts the user for an arity (a natural number) n and a word.
# Call symbol a word consisting of nothing but alphabetic characters
# and underscores.
# Checks that the word is valid, in that it satisfies the following
# inductive definition:
# - a symbol, with spaces allowed at both ends, is a valid word;
# - a word of the form s(w_1,...,w_n) with s denoting a symbol and
#   w_1, ..., w_n denoting valid words, with spaces allowed at both ends
#   and around parentheses and commas, is a valid word.


import sys
import re


def check_word(wd):
    # if wd is not empty and contains only alphabet then return True
    if re.match('^[A-Za-z_]+$', wd):
        return True
    return False


def is_valid(word, arity):
    # 1. count the number of ( and ) and see if they match,
    if word.count('(') != word.count(')'):
        if arity != 0 and word.count('(') == 0:
            return False

    # 2. to split the word, remove all of the blank first then put blank between () and ,
    word = word.replace(' ', '')
    word = word.replace(',', ' , ')
    word = word.replace('(', ' ( ')
    word = word.replace(')', ' ) ')

    # 3. split the word into multiple groups and remove all blank
    word_ls = list(word.split())
    print(word_ls)

    # 3.1 for arity = 0
    if arity == 0:
        if len(word_ls) != 1:
            return False
        else:
            return check_word(word_ls[0])

    # 4 check if the outer round is legal
    if arity >= 1 and len(word_ls) <= 1:
        return False
    else:
        if arity >= 1 and not word_ls[1] == '(' or not word_ls[-1] == ')':
            return False

    # 5. traverse the word_ls and check if the elements are legal
    pos = 0
    bracket_count = -1
    arity_num = []

    while pos in range(len(word_ls)):
        if word_ls[pos] == '(':
            bracket_count += 1
            arity_num.append(0)
        elif word_ls[pos] == ')':
            if arity_num[bracket_count] != arity:
                return False
            arity_num.pop(bracket_count)
            bracket_count -= 1
        elif word_ls[pos] == ',':
            if word_ls[pos + 1] == ',' or word_ls[pos + 1]==')' or pos == len(word_ls)-1:
                return False
        else:
            if not check_word(word_ls[pos]):
                return False
            else:
                if pos != 0:
                    arity_num[bracket_count] += 1
        pos += 1
    if bracket_count != -1:
        return False
    return True
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE


try:
    arity = int(input('Input an arity : '))
    if arity < 0:
        raise ValueError
except ValueError:
    print('Incorrect arity, giving up...')
    sys.exit()
word = input('Input a word: ')
if is_valid(word, arity):
    print('The word is valid.')
else:
    print('The word is invalid.')
