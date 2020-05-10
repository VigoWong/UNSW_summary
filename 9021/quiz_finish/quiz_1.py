# COMP9021 19T3 - Rachid Hamadi
# Quiz 1 *** Due Thursday Week 2


import sys
from random import seed, randrange


try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
mapping = {}
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 2, upper_bound)
    if r > 0:
        mapping[i] = r
print('\nThe generated mapping is:')
print('  ', mapping)

mapping_as_a_list = []
one_to_one_part_of_mapping = {}
nonkeys = []
map_len = len(mapping)
# INSERT YOUR CODE HERE
# 1
for k in range(1, upper_bound):
    if k not in mapping.keys():
        nonkeys.append(k)

# 2
for i in range(0, upper_bound):
    a = mapping.get(i, None)
    mapping_as_a_list.append(a)

# 3
# delete index in mapping with repeated value
one_to_one_part_of_mapping = mapping
repeat_keys = []
for k_1, v_1 in mapping.items():
    for k_2, v_2 in mapping.items():
        if k_1 != k_2 and v_1 == v_2:
            repeat_keys.append(k_1)

repeat_keys = set(repeat_keys)
for key in repeat_keys:
    one_to_one_part_of_mapping.pop(key)


print('\nThe mappings\'s so-called "keys" make up a set whose number of elements is', str(map_len)+'.')
print('\nThe list of integers between 1 and', upper_bound - 1, 'that are not keys of the mapping is:')
print('  ', nonkeys)
print('\nRepresented as a list, the mapping is:')
print('  ', mapping_as_a_list)
# Recreating the dictionary, inserting keys from smallest to largest,
# to make sure the dictionary is printed out with keys from smallest to largest.
one_to_one_part_of_mapping = {key: one_to_one_part_of_mapping[key]
                                      for key in sorted(one_to_one_part_of_mapping)
                             }
print('\nThe one-to-one part of the mapping is:')
print('  ', one_to_one_part_of_mapping)


