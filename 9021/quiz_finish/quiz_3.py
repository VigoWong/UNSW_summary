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
from copy import deepcopy
import sys

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
# 1. convert the code to octonary number and stored it with a list
oct_code = list('0' * nb_of_leading_zeroes + f'{int(code):o}')

# 2. build a map by model the move of command
pos = [0, 0]
pos_ls = [[0, 0]]
for i in range(1, len(oct_code) + 1):
    if oct_code[-i] == '0':
        pos[1] += 1
    elif oct_code[-i] == '1':
        pos[0] += 1
        pos[1] += 1
    elif oct_code[-i] == '2':
        pos[0] += 1
    elif oct_code[-i] == '3':
        pos[0] += 1
        pos[1] -= 1
    elif oct_code[-i] == '4':
        pos[1] -= 1
    elif oct_code[-i] == '5':
        pos[0] -= 1
        pos[1] -= 1
    elif oct_code[-i] == '6':
        pos[0] -= 1
    elif oct_code[-i] == '7':
        pos[0] -= 1
        pos[1] += 1
    pos_ls.append(deepcopy(pos))

# 2.1 calculate the width and height of the map
x_ls, y_ls = zip(*pos_ls)
width = max(x_ls) - min(x_ls) + 1
height = max(y_ls) - min(y_ls) + 1
map = [[off for i in range(width)] for k in range(height)]

# 3.confirm the poses that are white or black
# 3.1 move the coordinate to match the natural two-dimension array
if min(x_ls) < 0:
    minus = min(x_ls)
    x_ls = [x - minus for x in x_ls]
if max(y_ls) > 0:
    plus = max(y_ls)
    y_ls = [y - plus for y in y_ls]
pos_ls = list(zip(x_ls, y_ls))

#
for pos in pos_ls:
    if pos_ls.count(pos) % 2 != 0:
        map[-pos[1]][pos[0]] = on
    else:
        map[-pos[1]][pos[0]] = off

# remove rows that contain only "off"
start = 0
while start <= len(map)-1 and on not in map[start]:
    map[start].clear()
    start += 1

last = len(map) - 1
while last >= 0 and on not in map[last]:
    map[last].clear()
    last -= 1

# remove first several columns that contain only "off"
while True:
    column = []
    for i in range(height):
        if map[i]:
            column.append(map[i][0])
    for i in range(height):
        if on not in column and map[i]:
            map[i].pop(0)
    else:
        break

# remove latter several columns that contain only "off"
while True:
    column = []
    for i in range(height):
        if map[i]:
            column.append(map[i][-1])
    for i in range(height):
        if on not in column and map[i]:
            map[i].pop(-1)
    else:
        break

for i in map:
    if i:
        for l in i:
            print(l, end='')
        print()

    
