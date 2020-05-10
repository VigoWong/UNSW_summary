# COMP9021 19T3 - Rachid Hamadi
# Quiz 3 *** Due Thursday Week 4


# Reading the number written in base 8 from right to left,
# keeping the leading 0's, if any:
# 0: move N     1: move NE    2: move E     3: move SE
# 4: move S     5: move SW    6: move W     7: move NW
#
# We start from a position that is the unique position
# where the switch is on.
#
# Moving to a position switches on to off, off to on there.

import sys
from copy import copy

on = '\u26aa'
off = '\u26ab'
code = input('Enter a non-strictly negative integer: ').strip()
try:
    if code[0] == '-':
        raise ValueError
    int(code)
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
nb_of_leading_zeroes = 0
for i in range(len(code) - 1):
    if code[i] == '0':
        nb_of_leading_zeroes += 1
    else:
        break
print("Keeping leading 0's, if any, in base 8,", code, 'reads as',
      '0' * nb_of_leading_zeroes + f'{int(code):o}.'
      )
print()

# INSERT YOUR CODE HERE
# 1. convert the command to common sequence
command = list(reversed('0' * nb_of_leading_zeroes + f'{int(code):o}'))

# 2. record the position
pos_ls = [[0, 0], ]
cur_pos = [0, 0]
for i in command:
    if i in ['0', '1', '7']:
        cur_pos[1] += 1
    if i in ['3', '4', '5']:
        cur_pos[1] -= 1
    if i in ['1', '2', '3']:
        cur_pos[0] += 1
    if i in ['5', '6', '7']:
        cur_pos[0] -= 1
    pos_ls.append(copy(cur_pos))

# 3. remove pos in pos_ls that time of appearance more than or equal to 2
for i in pos_ls:
    if pos_ls.count(i) >= 2 and pos_ls.count(i)%2==0:
        while i in pos_ls:
            pos_ls.remove(i)

# 4. count the boundary of the map and adjust the axis
if pos_ls:
    x,y = list(zip(*pos_ls))
    y = [-i for i in y]
    pos_ls=list(zip(x,y))

# 5. print the map
if pos_ls:
    for l in range(min(y), max(y) + 1):
        for w in range(min(x), max(x) + 1):
            if (w, l) in pos_ls:
                print(on, end='')
            else:
                print(off, end='')
        print()
