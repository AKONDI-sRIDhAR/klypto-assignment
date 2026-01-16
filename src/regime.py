from hmmlearn import hmm
import pandas as pd
import numpy as np
import joblib

class RegimeModel:
    def __init__(self, n_states=3):
        self.model = hmm.GaussianHMM(n_components=n_states, covariance_type="full", n_iter=1000, random_state=42)
        
    def fit(self, X):
        self.model.fit(X)
        
    def predict(self, X):
        return self.model.predict(X)
        
    def save(self, path):
        joblib.dump(self.model, path)
        
    def load(self, path):
        self.model = joblib.load(path)
