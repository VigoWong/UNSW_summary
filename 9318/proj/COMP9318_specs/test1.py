import numpy as np

a = np.array([[1,2,3],[4,5,6],[1,3,5],[1,2,3]])
b = 2
# c = np.where((a[:, 1] == b))
# print(c)
d = np.argwhere((a[:, 1] == b)).T.tolist()[0]
print(a[np.ix_(d)])

for p in range(P):
    ls_from_code_index = np.argwhere((codes[:, p] == cluster_ls[p])).T.tolist()[0]
    ls_from_code = codes[np.ix_(ls_from_code_index)].tolist()

    for l in ls_from_code:
        dist_ls = []
        for a in range(P):
            dist = sorted_component_arr[a][component_indexes[a].index(l[a])]
            dist_ls.append(dist)
        s = sum(dist_ls)
        sum_dict[s] = [l]