# COMP9021 19T3 - Rachid Hamadi
# Sample Exam Question 5


'''
Will be tested with year between 1913 and 2013.
You might find the reader() function of the csv module useful,
but you can also use the split() method of the str class.
'''

import csv

def f(year):
    '''
    >>> f(1914)
    In 1914, maximum inflation was: 2.0
    It was achieved in the following months: Aug
    >>> f(1922)
    In 1922, maximum inflation was: 0.6
    It was achieved in the following months: Jul, Oct, Nov, Dec
    >>> f(1995)
    In 1995, maximum inflation was: 0.4
    It was achieved in the following months: Jan, Feb
    >>> f(2013)
    In 2013, maximum inflation was: 0.82
    It was achieved in the following months: Feb
    '''
    months = 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    month_inf = {i:0 for i in months}
    # Insert your code here
    o_ls = []
    max_inf = None
    with open('cpiai.csv', 'r') as f:
        for l in f.readlines():
            if l.startswith('Date'):
                continue
            date, ind, inf = l.strip().split(',')
            y,m,d = date.split('-')
            if y == str(year):
                month_inf[months[int(m)-1]] = float(inf)
        max_inf = max(month_inf.values())
        for k in month_inf:
            if month_inf[k] == max_inf:
                o_ls.append(k)
        o = ', '.join(o_ls)
    print(f'In {year}, maximum inflation was: {max_inf}')
    print(f'It was achieved in the following months: {o}')
                
             
            


if __name__ == '__main__':
    import doctest
    doctest.testmod()
