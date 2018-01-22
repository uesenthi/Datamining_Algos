import pandas as pd 
import numpy as np 

data = pd.read_csv('creditcard.csv')

data.isnull().any() #Checks to see if there are any null values inside within the table. If there were, you would drop the row
print data.dtypes