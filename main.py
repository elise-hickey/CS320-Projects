# project: p7
# submitter: ejhickey3
# partner: none
# hours: 5
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.pipeline import Pipeline
import pandas as pd

class UserPredictor:
    def __init__(self):
        self.model = Pipeline([
    ("pf", PolynomialFeatures(degree=2, include_bias=False)),
    ("std", StandardScaler()),
    ("lr", LogisticRegression(fit_intercept=True, max_iter=1000)),
])    
    def fit(self, ds1, ds2, ds3):
        sum_sec = {}
        user_id_ds = ds2.set_index("user_id")
        for num in range(len(ds1)):
            try:
                sum_sec[num] = user_id_ds.loc[num]["seconds"].sum()
            except:
                sum_sec[num] = 0 
        sum_sec = pd.Series(sum_sec)
        ds1 = ds1.set_index('user_id')
        ds1["seconds"] = sum_sec
        fit = self.model.fit(ds1[['age', 'past_purchase_amt', "seconds"]], ds3["y"])
        self.fit = fit
        
    def predict(self, tester1, tester2):
        sum_sec = {}
        user_id_ds = tester2.set_index("user_id")
        for num in list(tester1['user_id']):
            try:
                sum_sec[num] = user_id_ds.loc[num]["seconds"].sum()
            except:
                sum_sec[num] = 0
        sum_sec = pd.Series(sum_sec)
        tester1 = tester1.set_index('user_id')
        tester1["seconds"] = sum_sec
        predict = self.model.predict(tester1[['age', 'past_purchase_amt', "seconds" ]])
        return predict        
    
    