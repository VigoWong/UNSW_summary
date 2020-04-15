import submission
import pickle
import time

# How to run your implementation for Part 1
Total_case_num = 4
for i in range(1, Total_case_num + 1):
    with open(f'./data/new_data{i}', 'rb') as f:
        Data_File = pickle.load(f, encoding = 'bytes')
    with open(f'./data/new_centroids{i}', 'rb') as f:
        Centroids_File = pickle.load(f, encoding = 'bytes')
    codebooks, codes = submission.pq(Data_File, P=4, init_centroids=Centroids_File, max_iter = 20)
    
    with open(f'./data/result_Codebooks{i}', 'rb') as f:
        Result_codebooks = pickle.load(f, encoding = 'bytes')
    with open(f'./data/result_Codes{i}', 'rb') as f:
        Result_codes = pickle.load(f, encoding = 'bytes')
    
    flag_cb = (Result_codebooks == codebooks).all()
    flag_c = (Result_codes == codes).all()
    if flag_cb and flag_c:
        print(f'Test {i}: pass')
    else:
        if not flag_cb:
            print(f'Test {i}: The codebooks are different.')
        if not flag_c:
            print(f'Test {i}: The codes are different.')
        print()
    
        with open(f'./data/My_result_Codebooks{i}', 'wb') as file:
            pickle.dump(codebooks, file)
        with open(f'./data/My_result_Codes{i}', 'wb') as file:
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