# COMP9021 19T3 - Rachid Hamadi
# Quiz 6 *** Due Thursday Week 8
#
# Randomly fills an array of size 10x10 with 0s and 1s, and outputs the size of
# the largest parallelogram with horizontal sides.
# A parallelogram consists of a line with at least 2 consecutive 1s,
# with below at least one line with the same number of consecutive 1s,
# all those lines being aligned vertically in which case the parallelogram
# is actually a rectangle, e.g.
#      111
#      111
#      111
#      111
# or consecutive lines move to the left by one position, e.g.
#      111
#     111
#    111
#   111
# or consecutive lines move to the right by one position, e.g.
#      111
#       111
#        111
#         111


from random import seed, randrange
import sys

dim = 10


def display_grid():
    for row in grid:
        print('   ', *row)


def downing_find_max(grid, r, c, width):
    height = 1
    while True:
        # calculate the height
        r += 1
        if r > 9:
            break
        if 0 in [i for i in grid[r][c:(c + width)]]:
            break
        else:
            height += 1
    if height != 1:
        max = height * width
    else:
        max = 0
    return max


def right_downing_find_max(grid, r, c, width):
    height, e = 1, 0
    while True:
        # calculate the height
        r += 1
        e += 1
        if r > 9 or (c + width + e) > 9:
            break
        if 0 in [i for i in grid[r][(c + e):(c + width + e)]]:
            break
        else:
            height += 1
    if height != 1:
        max = height * width
    else:
        max = 0
    return max


def left_downing_find_max(grid, r, c, width):
    height, e = 1, 0
    while True:
        # calculate the height
        r += 1
        e -= 1
        if r > 9 or (c + e) < 0:
            break
        if 0 in [i for i in grid[r][(c + e):(c + e + width)]]:
            break
        else:
            height += 1
    if height != 1:
        max = height * width
    else:
        max = 0
    return max


def size_of_largest_parallelogram(grid):
    # traverse the whole list grid to find the parallelogram from top to bottom
    max_size = 0  # the max_size of the parallelogram
    r, c = 0, 0  # the position of the current row
    while r in range(len(grid)):
        c = 0
        # traverse every row to find the max parallelogram
        while c in range(len(grid[r]) - 1):
            # traverse a row from left most to right
            if grid[r][c] == 1 and grid[r][c + 1] == 1:  # if parallelogram can be made then get
                width = 2
                while True:
                    # base on a fixed elements,width +1 everytime and calculate the width and the max
                    if c + width - 1 <= 9:
                        if grid[r][c + width - 1] == 0:
                            break
                        cur_max = max(downing_find_max(grid, r, c, width),
                                      right_downing_find_max(grid, r, c, width),
                                      left_downing_find_max(grid, r, c, width))
                        if cur_max > max_size:
                            max_size = cur_max
                        width += 1
                    else:
                        break
            c += 1
        r += 1
    return max_size


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
size = size_of_largest_parallelogram(grid)
if size:
    print('The largest parallelogram with horizontal sides '
          f'has a size of {size}.'
          )
else:
    print('There is no parallelogram with horizontal sides.')
