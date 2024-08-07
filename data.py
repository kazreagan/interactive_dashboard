import pandas as pd

#importing the data
file_path = 'd:\Desktop\story time\Student_expenses.xlsx'
data = pd.read_excel(file_path, sheet_name='Data')

#data cleaning
data.drop_duplicates(inplace=True)
data.fillna(method='ffill', inplace=True)

#data inspection
data.head()