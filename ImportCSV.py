import pandas as pd
import numpy as np

data = pd.read_excel('commercial rent.xlsx')
mColumns = data.columns
# print(data.values)
for row in data.values:
    print((row[0]))
print(mColumns)
