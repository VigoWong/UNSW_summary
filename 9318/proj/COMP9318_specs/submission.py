# Created by Haowei Huang on 3 April, 2019

import numpy as np
from scipy import spatial
import pickle
import time


def k_means(data, init_centroid, max_iter, k):
    '''
    :param data:
    :param init_centroid: initialized centroid given by parameters
    :param max_iter: times of iteration
    :param k: number of clusters
    :return:
    '''
    # current centroid list is set to be the initialized one, the parameter of k-means
    cur_centroid = init_centroid.copy()

    if max_iter == 0:
        # update the distance between data points and centroid
        distance_matrix = spatial.distance.cdist(data, cur_centroid, metric='cityblock')
        # find the nearest centroid of each data point and record the index of the centroid
        code = np.argmin(distance_matrix, axis=1)

        return init_centroid, code

    else:
        code = None
        for i in range(max_iter):
            # update the distance between data points and centroid
            distance_matrix = spatial.distance.cdist(data, cur_centroid, metric='cityblock')
            # find the nearest centroid of each data point and record the index of the centroid
            code = np.argmin(distance_matrix, axis=1)
            # update the current centroid
            cur_centroid = np.array([np.median(data[j == code], axis=0) if j in code else cur_centroid[j] for j in range(k)])

        return cur_centroid, code


def pq(data, P, init_centroids, max_iter):
    '''
    :param data: an array with shape (N,M) and dtype='float32',
            where N(rows) is the number of vectors and M(columns) is the dimensionality.
    :param P: the number of partitions/blocks the vector will be split into
    :param init_centroids: an array with shape (P,K,M/P) and dtype='float32'
    :param max_iter: is the maximum number of iterations of the K-means clustering algorithm
    :return:
    1. codebooks is an array with shape (P, K, M/P) and dtype='float32',
    which corresponds to the PQ codebooks for the inverted multi-index.
     E.g., there are P codebooks and each one has K M/P-dimensional codewords.
    2. codes is an array with shape (N, P) and dtype=='uint8', which corresponds to the codes for the data vectors.
    The dtype='uint8' is because K is fixed to be 256 thus the codes should integers between 0 and 255.
    '''

    # split the array according to P, and train different dimensions seperately
    N = data.shape[0]  # number of data points
    data = np.split(data, P, axis=1)

    codebooks = init_centroids.copy()
    codes = np.empty([P, N], dtype='uint8', order='C')

    # do cluster by k-means to get the code books and code
    for i in range(P):
        codebooks[i], codes[i] = k_means(data[i], init_centroids[i], max_iter, len(init_centroids[i]))

    return codebooks, codes.T


def query(queries, codebooks, codes, T):
    '''
    :param queries: queries is an array with shape (Q, M) and dtype='float32',
    where Q is the number of query vectors and M is the dimensionality.
    :param codebooks: codebooks is an array with shape (P, K, M/P) and dtype='float32',
    which corresponds to the codebooks returned by pq() in part 1.
    :param codes: codes is an array with shape (N, P) and dtype=='uint8',
    which corresponds to the codes returned by pq() in part 1.
    :param T: the minimum candidate numbers
    :return: candidate list of queries
    '''

    # number of partitions
    P = codebooks.shape[0]
    # the returned list
    ret_ls = []
    for q in queries:
        # split the queries and codes into partitions and cope with partitions respectively
        q = np.split(np.array([q]), P, axis=1)
        # for each partition, simply make a generator to cope with the query
        component_arr = []
        sorted_component_arr = []
        component_indexes = []

        for p in range(P):
            dist_arr = spatial.distance.cdist(np.array(q[p]), codebooks[p], metric='cityblock')
            # calculate all possible ADs
            component_arr.append(dist_arr.tolist()[0])
            # initialize a generator, producing minial AD and the corresponding cluster index
            index_arr = np.argsort(dist_arr)
            sorted_component_arr.append(sorted(component_arr[p]))
            component_indexes.append(index_arr.tolist()[0])

        # initialize a candidates set
        candidate_set = set()
        # list of tuples formatted (distance, candidate)
        cur_ls = [[sorted_component_arr[p][0], component_arr[p].index(sorted_component_arr[p][0])] for p in range(P)]
        # the number of candidates of each query should not be less than T
        dist_ls, cluster_ls = zip(*cur_ls)
        cluster_ls = list(cluster_ls)
        sum_dict = {sum(dist_ls): [cluster_ls]}  # formatted key: distance, value: clusters

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

        while len(candidate_set) < T:
            print(cluster_ls)

            sum_ls = sum_dict.keys()
            next_ADsum = sorted(sum_ls, reverse = True).pop()
            cluster_ls = sum_dict[next_ADsum]
            sum_dict.pop(next_ADsum)

            # find data points whose cluster ls match the corresponding code
            for ls in cluster_ls:
                candidates = set(np.where((codes == ls).all(1))[0])
                candidate_set = candidate_set | candidates

            for ls in cluster_ls:
                for i in range(len(ls)):
                    # get next value of partition i
                    # component_arr, sorted_component_arr ,component_indexes
                    # cur_index = component_indexes[i].index(ls[i])
                    # next_index = cur_index + 1
                    # if next_index > 255: continue
                    # next_clu = component_indexes[i][next_index]
                    # next_AD = sorted_component_arr[i][next_index]
                    #
                    #
                    # dist = sorted_component_arr[i][component_indexes[i].index(ls[i])]
                    # newDistance = next_ADsum - dist + next_AD
                    # cur_cluls = ls.copy()
                    # cur_cluls[i] = next_clu
                    #
                    # if newDistance not in sum_dict.keys():
                    #     sum_dict[newDistance] = [cur_cluls]
                    # else:
                    #     sum_dict[newDistance].append(cur_cluls)
                    cur_index = component_indexes[i].index(ls[i])
                    next_index = cur_index + 1
                    next_clu = component_indexes[i][next_index]


                    ls_from_code_index = np.argwhere((codes[:, 1] == next_clu)).T.tolist()[0]
                    ls_from_code = codes[np.ix_(ls_from_code_index)].tolist()
                    for l in ls_from_code:
                        dist_ls = []
                        for a in range(P):
                            dist = sorted_component_arr[a][component_indexes[a].index(l[a])]
                            dist_ls.append(dist)
                        s = sum(dist_ls)
                        if s in sum_dict:
                            sum_dict[s].append(l)
                        else:
                            sum_dict[s] = [l]



        ret_ls.append(candidate_set)

    return ret_ls


if __name__ == '__main__':
    np.set_printoptions(threshold=np.inf)
    start = time.time()
    with open('./test/data/new_data1', 'rb') as f:
        Data_File = pickle.load(f, encoding='bytes')
    with open('./test/data/new_centroids1', 'rb') as f:
        Centroids_File = pickle.load(f, encoding='bytes')

    P = len(Centroids_File)
    codebooks, codes = pq(Data_File, P, init_centroids=Centroids_File, max_iter=20)
    print(codes)
    print('-------------------------------------------------------------------------------------')
    with open('./test/data/myresult/result_Codes1', 'rb') as f:
        code_result = pickle.load(f, encoding='bytes')
    print(code_result)
    print((codes == code_result))

    # end = time.time()
    # time_cost_1 = end - start
    # print(time_cost_1)
    # # with open('./test/data/myoutput/output_Codebooks1', 'wb') as f:
    # #     pickle.dump(codebooks, f)
    # # with open('./test/data/myoutput/output_Codes1', 'wb') as f:
    # #     pickle.dump(codes, f)
    # #
    # # with open('./test/data/myresult/result_Codebooks1', 'rb') as f:
    # #     codebooks_result = pickle.load(f, encoding='bytes')
    # # with open('./test/data/myoutput/output_Codebooks1', 'rb') as f:
    # #     codebooks_out = pickle.load(f, encoding='bytes')
    # # with open('./test/data/myresult/result_Codes1', 'rb') as f:
    # #     codes_result = pickle.load(f, encoding='bytes')
    # # with open('./test/data/myoutput/output_Codes1', 'rb') as f:
    # #     codes_out = pickle.load(f, encoding='bytes')
    # with open('./codebooks1', 'rb') as f:
    #     codebooks = pickle.load(f, encoding='bytes')
    # with open('./codes1', 'rb') as f:
    #     codes = pickle.load(f, encoding='bytes')
    #
    #
    # # a = set(codes[:, 0].T)
    # # a = 1
    #
    # # How to run your implementation for Part 2
    # with open('./toy_example/Query_File', 'rb') as f:
    #     Query_File = pickle.load(f, encoding='bytes')
    # # queries = pickle.load(Query_File, encoding='bytes')
    # # start = time.time()
    # # print(Query_File)
    # candidates = query(Query_File, codebooks, codes, T=10)
    # end = time.time()
    # time_cost_2 = end - start
    # # output for part 2.
    # print(candidates)
