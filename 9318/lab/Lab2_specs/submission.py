## import modules here 
import pandas as pd
import numpy as np
import helper
import itertools


################### Question 1 ###################
def buc_reduce_dim(confirm_arr, cur_df, ret_df):
    # base case, only the measure is left and just simply sum all records
    if cur_df.shape[1] == 1:
        sum = cur_df["M"].sum()
        confirm_arr.append(sum)
        ret_df.loc[ret_df.shape[0]] = confirm_arr
        return ret_df
    # to avoid unnecessary computing, when there is a single tuple, computing all of combinations answers iteratively
    if cur_df.shape[0] == 1:
        dims = cur_df.shape[1] -1
        for i in range(dims+1):
            for j in itertools.combinations(range(dims), i):
                new_r = list(cur_df.iloc[0])
                for k in j:
                    new_r[k] = "ALL"
                ret_df.loc[ret_df.shape[0]] = confirm_arr+new_r
        return ret_df
    # for common case, select all possible value of the last dimension into confirmed arr and enter next recursion
    else:
        values = sorted(list(set(helper.project_data(cur_df, 0))))
        for v in values:
            ret_df = buc_reduce_dim(confirm_arr + [v], helper.slice_data_dim0(cur_df, v), ret_df)
        ret_df = buc_reduce_dim(confirm_arr + ["ALL"], helper.remove_first_dim(cur_df), ret_df)
        return ret_df


def buc_rec_optimized(df):  # do not change the heading of the function
    ret_df = df.iloc[0:0].copy()
    buc_reduce_dim([], df, ret_df)
    return ret_df

if __name__ == '__main__':
    input_data = helper.read_data('./testing/tests/09_test.txt')
    output = buc_rec_optimized(input_data)
    print(output)
    output.to_csv('./NEW.txt', sep='\t', index=False)