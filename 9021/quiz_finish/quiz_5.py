# COMP9021 19T3 - Rachid Hamadi
# COMP9021 19T3 - Rachid Hamadi
# Quiz 5 *** Due Thursday Week 7
#
# Implements a function that, based on the encoding of
# a single strictly positive integer that in base 2,
# reads as b_1 ... b_n, as b_1b_1 ... b_nb_n, encodes
# a sequence of strictly positive integers N_1 ... N_k
# with k >= 1 as N_1* 0 ... 0 N_k* where for all 0 < i <= k,
# N_i* is the encoding of N_i.
#
# Implements a function to decode a positive integer N
# into a sequence of (one or more) strictly positive
# integers according to the previous encoding scheme,
# or return None in case N does not encode such a sequence.


import sys
import collections


def encode(list_of_integers):
    list_of_integers = [bin(i)[2:] for i in list_of_integers]
    pre_ls = []
    pre_num = ''
    for i in list_of_integers:
        pre_int = ''
        for k in i:
            pre_int += 2*k
        pre_ls.append(pre_int)
    for i in range(len(pre_ls)):
        if i != len(pre_ls) - 1:
            pre_num += (pre_ls[i]+ '0')
        else:
            pre_num += pre_ls[i]
    return int(pre_num,2)


def decode(integer):
    input_num = str(bin(integer)[2:])
    i, group_num = 0, 0
    group_bin_ls = collections.defaultdict(list)
    group_ls = []
    while i in range(len(input_num)):
        if i != len(input_num)-1:
            if input_num[i] == input_num[i + 1]:
                group_bin_ls[group_num].append(input_num[i])
                i += 2
            else:
                if input_num[i]=='0':
                    i += 1
                    group_num+=1
                else:
                    return None
        else:
            return None
    for g in group_bin_ls.values():
        group_ls.append(int(''.join(g),2))
    if group_ls:
        return group_ls
    else:
        return None
    # We assume that user input is valid. No need to check


# for validity, nor to take action in case it is invalid.
print('Input either a strictly positive integer')
the_input = eval(input('or a nonempty list of strictly positive integers: '))
if type(the_input) is int:
    print('  In base 2,', the_input, 'reads as', bin(the_input)[2:])
    decoding = decode(the_input)
    if decoding is None:
        print('Incorrect encoding!')
    else:
        print('  It encodes: ', decode(the_input))
else:
    print('  In base 2,', the_input, 'reads as',
          f'[{", ".join(bin(e)[2:] for e in the_input)}]'
          )
    print('  It is encoded by', encode(the_input))

