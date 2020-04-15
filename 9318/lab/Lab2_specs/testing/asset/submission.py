## import modules here 
import pandas as pd
import numpy as np
import helper


################### Question 1 ###################
def buc_reduce_dim(confirm_arr, cur_df, ret_df, generator):
    # base case, only one dimension is left and just simply add all record on the returned df as well as the sum record
    if cur_df.shape[1] == 1:
        sum = cur_df.iloc[-1].sum()
        confirm_arr.append(sum)
        ret_df.loc[next(generator)] = confirm_arr
        return ret_df
    else:
        values = sorted(list(set(helper.project_data(cur_df, 0))))
        # sorted(list(set(project_data(df, 0))))

        for v in values:
            ret_df = buc_reduce_dim(confirm_arr + [v], helper.slice_data_dim0(cur_df, v), ret_df, generator)
        ret_df = buc_reduce_dim(confirm_arr+["All"], helper.remove_first_dim(cur_df), ret_df, generator)
        return ret_df


def buc_rec_optimized(df):# do not change the heading of the function
    generator = (x for x in range(df.shape[1] ** 2))
    ret_df = df.iloc[0:0].copy()
    ret = buc_reduce_dim([], df, ret_df, generator)
    return ret
