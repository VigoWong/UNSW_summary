# COMP9021 19T3 - Rachid Hamadi
# Quiz 7 *** Due Thursday Week 9
#
# Randomly generates a grid of 0s and 1s and determines
# the maximum number of "spikes" in a shape.
# A shape is made up of 1s connected horizontally or vertically (it can contain holes).
# A "spike" in a shape is a 1 that is part of this shape and "sticks out"
# (has exactly one neighbour in the shape).
from copy import copy
from random import seed, randrange
import sys

dim = 10


def display_grid():
    for row in grid:
        print('   ', *row)

    # Returns the number of shapes we have discovered and "coloured".


# We "colour" the first shape we find by replacing all the 1s
# that make it with 2. We "colour" the second shape we find by
# replacing all the 1s that make it with 3.
def expand(grid, ls):
    while True:
        new_ls = ls
        for i in ls:
            if (i[1] + 1) <= 9 and grid[i[0]][i[1] + 1] == 1 and [i[0], i[1] + 1] not in ls:
                new_ls.append([i[0], i[1] + 1])
            if (i[0] + 1) <= 9 and grid[i[0] + 1][i[1]] == 1 and [i[0] + 1, i[1]] not in ls:
                new_ls.append([i[0] + 1, i[1]])
            if (i[0] - 1) >= 0 and grid[i[0] - 1][i[1]] == 1 and [i[0] - 1, i[1]] not in ls:
                new_ls.append([i[0] - 1, i[1]])
            if (i[1] - 1) >= 0 and grid[i[0]][i[1] - 1] == 1 and [i[0], i[1] - 1] not in ls:
                new_ls.append([i[0], i[1] - 1])
        if new_ls == ls:
            break
    return new_ls


def colour_shapes(grid):
    # traverse every element to find the ls of shapes
    visited_ls = []
    shape_ls = []
    for r in range(len(grid)):
        c = 0
        for c in range(len(grid[r])):
            if grid[r][c] and [r, c] not in visited_ls:
                ex_shape = expand(grid, [[r, c]])
                shape_ls.append(ex_shape)
                for e in ex_shape:
                    visited_ls.append(e)
            else:
                continue
    return shape_ls


def max_number_of_spikes(shape_ls):
    count_ls = []
    for s in shape_ls:
        if len(s)>1:
            spikes_num = 0
            for i in s:
                count = 0
                if [i[0] + 1, i[1]] in s:
                    count += 1
                if [i[0] - 1, i[1]] in s:
                    count += 1
                if [i[0], i[1] + 1] in s:
                    count += 1
                if [i[0], i[1] - 1] in s:
                    count += 1
                if count == 1:
                    spikes_num += 1
            count_ls.append(spikes_num)
    return max(count_ls)


try:
    for_seed, density = (int(x) for x in input('Enter two integers, the second '
                                               'one being strictly positive: '
                                               ).split()
                         )
    if density <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[int(randrange(density) != 0) for _ in range(dim)]
        for _ in range(dim)
        ]
print('Here is the grid that has been generated:')
display_grid()
nb_of_shapes = colour_shapes(grid)
print('The maximum number of spikes of some shape is:',
      max_number_of_spikes(nb_of_shapes)
      )
