import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

class mytransformer(BaseEstimator, TransformerMixin):
    
	def __init__(self):
		print('hello')
        
	def fit(self, X, y = None):
		print("fit!")
		return self


	def transform(self, X, y = None):
		print("transform")
		df = X
		df['timestamp'] = pd.to_datetime(df[["year", "month", "day", "hour", "minute"]])
		temp=df.drop(['year','month','day','hour','minute'],axis=1)
		temp1=temp.set_index('timestamp')
		tt=temp1.groupby(['loggername',pd.Grouper(freq='H')]).aggregate(np.sum)
		tt1=tt.reset_index().pivot('timestamp','loggername','power').rename_axis(index=None,columns=None)
		tt2=tt1.fillna(0)
		tt2[tt2 < 0] = 0
		tt2.reset_index(inplace=True)
		tt3=tt2.std(axis=1)
		df=pd.DataFrame(tt3)
		return df.values


 
