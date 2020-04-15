import submission
import pickle
import time

# How to run your implementation for Part 1
with open('./data/new_data4', 'rb') as f:
    Data_File = pickle.load(f, encoding = 'bytes')
with open('./data/new_centroids4', 'rb') as f:
    Centroids_File = pickle.load(f, encoding = 'bytes')
start = time.time()
codebooks, codes = submission.pq(Data_File, P=4, init_centroids=Centroids_File, max_iter = 20)


end = time.time()
time_cost_1 = end - start
print(time_cost_1)

with open('./data/result_Codebooks4', 'wb') as file:
        pickle.dump(codebooks, file)
with open('./data/result_Codes4', 'wb') as file:
        pickle.dump(codes, file)

# # How to run your implementation for Part 2
# with open('./toy_example/Query_File', 'rb') as f:
#     Query_File = pickle.load(f, encoding = 'bytes')
# queries = pickle.load(Query_File, encoding = 'bytes')
# start = time.time()
# candidates = submission.query(queries, codebooks, codes, T=10)
# end = time.time()
# time_cost_2 = end - start

# # output for part 2.
# print(candidates)


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

        for p in range(P):
            # calculate all possible ADs
            component_arr.append(spatial.distance.cdist(np.array(q[p]), codebooks[p], metric='cityblock').tolist()[0])
            # initialize a generator, producing minial AD and the corresponding cluster index
            sorted_component_arr.append(sorted(component_arr[p]))

        # initialize a candidates set
        candidate_set = set()
        # list of tuples formatted (distance, candidate)
        count_ls = [1 for i in range(P)]
        cur_ls = [(sorted_component_arr[p][0], component_arr.index(sorted_component_arr[p][0])) for p in range(p)]
        next_ls = [(sorted_component_arr[p][1], component_arr.index(sorted_component_arr[p][1])) for p in range(p)]
        # the number of candidates of each query should not be less than T
        dist_ls, cluster_ls = zip(*cur_ls)
        # add all candidates belongs to the cluster of minimal AD
        for c in range(len(cluster_ls)):
            candidates = set(np.where(codes[:, c] == cluster_ls[c])[0])
            candidate_set = candidate_set | candidates

        while len(candidate_set) < T:
            # unzip the (distance, cluster) tuple
            dist_ls, cluster_ls = zip(*cur_ls)
            # get the difference of current AD and next AD of different partitions
            diff_ls = [next_ls[i][0] - cur_ls[i][0] for i in range(P)]
            # find the minimum diff and its cluster id
            index_tochange = diff_ls.index(min(diff_ls))
            # find data points in this cluster and add them in the candidates set
            candidates = set(np.where(codes[:, index_tochange] == cluster_ls[index_tochange])[0])
            candidate_set = candidate_set | candidates
            # update the value under the index of cur_ls and next_ls
            count_ls[index_tochange]+=1
            cur_ls[index_tochange] = next_ls[index_tochange]
            next_ls[index_tochange] = (sorted_component_arr[index_tochange][count_ls[index_tochange]],
                                       component_arr.index(sorted_component_arr[index_tochange][count_ls[index_tochange]]))

        # append the candidate set into the returned list
        ret_ls.append(candidate_set)
    print(ret_ls)
    return ret_ls



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

        for p in range(P):
            # calculate all possible ADs
            component_arr.append(spatial.distance.cdist(np.array(q[p]), codebooks[p], metric='cityblock').tolist()[0])
            # initialize a generator, producing minial AD and the corresponding cluster index
            sorted_component_arr.append(sorted(component_arr[p]))

        # initialize a candidates set
        candidate_set = set()
        # list of tuples formatted (distance, candidate)
        count_ls = [1 for i in range(P)]
        cur_ls = [(sorted_component_arr[p][0], component_arr[p].index(sorted_component_arr[p][0])) for p in range(P)]
        next_ls = [(sorted_component_arr[p][1], component_arr[p].index(sorted_component_arr[p][1])) for p in range(P)]
        # the number of candidates of each query should not be less than T
        dist_ls, cluster_ls = zip(*cur_ls)
        # add all candidates belongs to the cluster of minimal AD
        for c in range(len(cluster_ls)):
            candidates = set(np.where(codes[:, c] == cluster_ls[c])[0])
            candidate_set = candidate_set | candidates

        while len(candidate_set) < T:
            # unzip the (distance, cluster) tuple
            dist_ls, cluster_ls = zip(*cur_ls)
            # get the difference of current AD and next AD of different partitions
            diff_ls = [next_ls[i][0] - cur_ls[i][0] for i in range(P)]
            # find the minimum diff and its cluster id
            index_tochange = diff_ls.index(min(diff_ls))
            # find data points in this cluster and add them in the candidates set
            candidates = set(np.where(codes[:, index_tochange] == cluster_ls[index_tochange])[0])
            candidate_set = candidate_set | candidates
            # update the value under the index of cur_ls and next_ls
            count_ls[index_tochange]+=1
            cur_ls[index_tochange] = next_ls[index_tochange]
            next_ls[index_tochange] = (sorted_component_arr[index_tochange][count_ls[index_tochange]],
                                       component_arr[index_tochange].index(
                                           sorted_component_arr[index_tochange][count_ls[index_tochange]]))

        # append the candidate set into the returned list
        ret_ls.append(candidate_set)
    print(ret_ls)
    return ret_ls