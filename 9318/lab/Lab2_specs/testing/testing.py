from asset.submission import buc_rec_optimized
import os
import pandas as pd
import numpy as np
from collections import defaultdict
import time

test_directory = 'tests'
cube_directory = 'cubes'

def read_data(filename):
    df = pd.read_csv(filename, sep='\t')
    return (df)

def main():

    test_files = os.listdir(test_directory)
    cube_files = os.listdir(cube_directory)
    num_correct = 0
    for i in range(len(test_files)):
        counters = defaultdict(int)
    
        input_data = read_data(test_directory + '/' + test_files[i])
        
        start_time = time.perf_counter()
        output_data = buc_rec_optimized(input_data).astype(str).reset_index(drop=True).astype(str)
        stop_time = time.perf_counter()
        elapsed_time = stop_time - start_time
        print('{}: {:.3f} seconds'.format(test_files[i], elapsed_time))
        
        answer = read_data(cube_directory + '/' + cube_files[i]).astype(str)
        correct = np.sum(np.sum(output_data == answer)) == answer.shape[0] * answer.shape[1]
        
        try:
            if answer.shape[1] > 1:
                correct_2 = np.sum(np.sum(output_data.sort_values(by=list(output_data.columns[:-1]),ignore_index=True) == answer.sort_values(by=list(output_data.columns[:-1]),ignore_index=True))) == answer.shape[0] * answer.shape[1]
        except ValueError as e:
            print('cannot sort dataframe')
        
        if not correct:
            print('-' * 50)
            if correct_2:
                print('The cube data is correct, however, the order is not correct')
            print(test_files[i] + ' is not correct')
            print('\ninput data')
            print(input_data)
            print('\noutput data')
            print(output_data)
            print('\ntrue answer')
            print(answer)
            print('\ntrue and false')
            print(output_data == answer)
        else:
            num_correct += 1

    print('In total, ' + str(num_correct) + '/' + str(len(test_files)) + ' tests are correct.')

if __name__=='__main__':
    main()