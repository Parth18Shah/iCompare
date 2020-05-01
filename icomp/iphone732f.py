# import sklearn
from sklearn import linear_model
import numpy as np
import pandas as pd
import pickle
import warnings

warnings.filterwarnings("ignore")


iphone732 = pd.read_excel('iphone732.xlsx')
iphone732['Month'] = iphone732['Date'].apply(lambda time: time.month)
iphone732['Year'] = iphone732['Date'].apply(lambda time: time.year)
iphone732['Day'] = iphone732['Date'].apply(lambda time: time.day)
iphone732.drop('Date',inplace=True,axis=1)
X=iphone732[['Day','Month','Year']].iloc[0:1293].values
y=iphone732['Price'].values

lm = linear_model.LinearRegression()
lm.fit(X,y)
pickle.dump(lm,open('model_predict','wb'))
my_model = pickle.load(open('model_predict','rb'))
print(my_model.predict([[1,4,2020]]))