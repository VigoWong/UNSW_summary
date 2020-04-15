## import modules here
from collections import defaultdict
import numpy as np


################# Question 1 #################

def compute_error(data, labels, k):
    n, d = data.shape
    centers = []
    for i in range(k):
        centers.append([0 for j in range(d)])

    for i in range(n):
        centers[labels[i]] = [x + y for x, y in zip(centers[labels[i]], data[i])]

    error = 0
    for i in range(n):
        error += dot_product(centers[labels[i]], data[i])
    return error

def dot_product(a, b):
    res = 0
    for i in range(len(a)):
        res += a[i] * b[i]
    return res

def hc(data, k):  # do not change the heading of the function
    dic = defaultdict(list)
    # construct the triangle
    for i in range(len(data)):
        for j in range(len(data)):
            if i == j:
                dic[str(i)].append(1.0)
            else:
                dic[str(i)].append(dot_product(data[i], data[j]))

    # there will be (k - len(triangle)) loops
    for i in range(len(dic), k, -1):
        # acquire all values
        keys = list(dic.keys())
        array = np.array(list(dic.values()))
        # get the maximum values and ready to merge
        print(list(dic.values()))
        vals = sum(list(dic.values()), [])
        max_val = max([a for a in vals if a != 1.0])
        # get the indexes of two dimension needed to be merged(
        index_1, index_2 = np.where(array == max_val)
        r, c = min(index_1), max(index_1)
        new_t = array.copy()
        # merge r to y
        keys[c] += (','+keys[r])
        keys.remove(keys[r])
        for row in range(len(new_t)):
            for column in range(len(new_t[row])):
                if ((row == r or row == c) and column != r and column != c):
                    new_t[row][column] = min(array[r][column], array[c][column])
                if ((column == r or column == c) and row!=r and row != c):
                    new_t[row][column] = min(array[row][r], array[row][c])
        # then remove the r th row and r th column
        new_t= np.delete(new_t, r, axis=0)
        new_t = np.delete(new_t, r, axis=1)

        # assign new keys for the array
        dic = {keys[a]:list(new_t[a]) for a in range(len(new_t))}

    ret = []
    label = [i for i in range(len(data))]
    # compute the labels
    for i in dic.keys():
        ls = [int(a) for a in i.split(',')]
        ret.append(ls)

    for a in range(k):
        for b in ret[a]:
            label[b] = a

    return label


if __name__ == '__main__':
    data = np.loadtxt('asset/data.txt', dtype=float)
    print(hc(data, 2))

