



import pandas as pd

data = {'水果':['苹果','梨','草莓'],
       '数量':[3,2,5],
       '价格':[10,9,8]}
a = pd.DataFrame(data)
a['class'] = [1, 2 ,3 ]
print(a)
a['数量'][1] = 10
print(a)

    titles = df.columns.values.tolist()

    ham_df = df[df['class'] == 'ham']
    ham_sum_ls = ham_df.apply(sum)
    df.loc['sum'] = df.iloc[[i for i in range(len(training_data))]].map(sum)

    spam_df =  df.loc[df['class'] == 'spam']