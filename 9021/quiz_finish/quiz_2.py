# COMP9021 19T3 - Rachid Hamadi
# Quiz 2 *** Due Thursday Week 3


import sys
from random import seed, randrange
from pprint import pprint

try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
mapping = {}
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 8, upper_bound)
    if r > 0:
        mapping[i] = r
print('\nThe generated mapping is:')
print('  ', mapping)
# sorted() can take as argument a list, a dictionary, a set...
keys = sorted(mapping.keys())
print('\nThe keys are, from smallest to largest: ')
print('  ', keys)

cycles = []
reversed_dict_per_length = {}

# INSERT YOUR CODE HERE
# q1
for a in keys:
    cycle = []
    if a == mapping[a]:
        cycles.append([a])

    elif mapping[a] in keys:
        pos = None
        for i in range(len(keys)):
            if not pos:
                pos = a
            cycle.append(pos)
            if pos in keys:
                pos = mapping[pos]
            else:
                cycle.clear()
                break
            if pos == cycle[0]:
                break
            elif pos in cycle:
                cycle.clear()
                break
    for n in cycles:
        if cycle and cycle[0] in n:
            cycle.clear()
    if cycle:
        cycles.append(cycle)

# q2
vals = list(mapping.values())
len_ls = [vals.count(i) for i in vals]
val_len_map = {}
for i in range(len(vals)):
    val_len_map[vals[i]] = len_ls[i]
len_key = {len:{} for len in sorted((set(len_ls)))}
for a in len_key.keys():
    len_key[a] = {val:[key for key in keys if mapping[key] == val] for val in vals if val_len_map[val] == a}
for val in len_key.values():
    list(val).sort()
reversed_dict_per_length = len_key


print('\nProperly ordered, the cycles given by the mapping are: ')
print('  ', cycles)
print('\nThe (triply ordered) reversed dictionary per lengths is: ')
pprint(reversed_dict_per_length)


