import numpy as np
import pandas as pd

pd1=pd.DataFrame(np.arange(25).reshape(5,5))
pd2=pd.DataFrame()
print(pd1)
print(type(pd1.iloc[0]))
print(pd1.iloc[0])