import numpy as np
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
		return df.values