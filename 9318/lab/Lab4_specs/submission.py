## import modules here 

################# Question 1 #################
import pandas as pd
import numpy as np
from math import factorial


def tokenize(sms):
    return sms.split(' ')


def get_freq_of_tokens(sms):
    tokens = {}
    for token in tokenize(sms):
        if token not in tokens:
            tokens[token] = 1
        else:
            tokens[token] += 1
    return tokens


def multinomial_nb(training_data, sms):  # do not change the heading of the function
    '''
    :param training_data: list of tuples formatted (dict(word: timesOfAppearance), label)
    :param sms: query email
    :return: p(spam) / p(ham)
    '''
    df = pd.DataFrame()
    for t in range(len(training_data)):
        data, label = training_data[t][0], training_data[t][1]
        if t == 0:
            row = {w: {t: data[w]} for w in data.keys()}
            df = pd.DataFrame(row, dtype='int')
            continue
        df.loc[t] = 0
        k_ls = list(data.keys())
        for w in range(len(k_ls)):
            titles = df.columns.values.tolist()
            if k_ls[w] not in titles:
                df[k_ls[w]] = 0
            row = dict(df.iloc[t])
            row[k_ls[w]] += data[k_ls[w]]
            df.iloc[t] = pd.Series(row)
    df['class'] = [l[1] for l in training_data]
    titles = df.columns.values.tolist()[:-1]

    ham_df = df[df['class'] == 'ham'].iloc[:, :-1]
    ham_df.loc['sum'] = ham_df.apply(lambda x: x.sum() + 1, axis=0)
    print(ham_df)
    ham_dict = dict(ham_df.loc['sum'])
    ham_sum = sum(ham_dict.values())
    ham_dict = {x: y / ham_sum for x, y in ham_dict.items()}
    print(sum(ham_dict.values()))

    spam_df = df.loc[df['class'] == 'spam'].iloc[:, :-1]
    spam_df.loc['sum'] = spam_df.apply(lambda x: x.sum() + 1, axis=0)
    print(spam_df)
    spam_dict = dict(spam_df.loc['sum'])
    spam_sum = sum(spam_dict.values())
    spam_dict = {x: y / spam_sum for x, y in spam_dict.items()}
    print(sum(spam_dict.values()))

    valid_word = [w for w in sms if w in titles]
    sms_dict = {w: valid_word.count(w) for w in titles}
    q_len = sum(sms_dict.values())

    ham_val, spam_val = factorial(q_len), factorial(q_len)

    for k in titles:
        count = sms_dict[k]
        if ham_dict[k] == spam_dict[k]:
            continue
        ham_val *= ((ham_dict[k] ** (count+1)) / factorial((count+1)))
        spam_val *= ((spam_dict[k] ** (count+1)) / factorial((count+1)))

    return spam_val / ham_val


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    raw_data = pd.read_csv('./asset/data.txt', sep='\t')
    training_data = []
    for index in range(len(raw_data)):
        training_data.append((get_freq_of_tokens(raw_data.iloc[index].text), raw_data.iloc[index].category))
    sms = 'I am not spam'
    print(multinomial_nb(training_data, tokenize(sms)))
