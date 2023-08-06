from analysis_tools.common.util import *
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, StandardScaler


class DataProcessor:
    def __init__(self, X, y):
        self.X = X.copy()
        self.y = y.copy()

    ''
    ### Main method #########################################
    def preprocess(self, ord=None, nom=None):
        ## 1. Simple impute
        X = self.impute(self.X)

        ## 2. Process ord, nom, num
        X = self.process_ord(X, ord)
        X = self.process_nom(X, nom)
        X = self.process_num(X)

        ## 3. Split train, test data
        train = dict(X=X[self.y.notnull()], y=self.y[self.y.notnull()])
        test  = dict(X=X[self.y.isnull()], y=self.y[self.y.isnull()])
        return train, test
    def process_ord(self, X, ord):
        if ord is None:
            return X
        ord = [f for f in ord if f in X.columns]
        ord_enc = OrdinalEncoder()
        ord_enc.fit(X[ord])
        X[ord] = ord_enc.transform(X[ord])
        return X
    def process_nom(self, X, nom):
        if nom is None:
            return X
        nom = [f for f in nom if f in X.columns]
        onehot_enc = OneHotEncoder(sparse=False)
        onehot_enc.fit(X[nom])
        df_onehot = pd.DataFrame(onehot_enc.transform(X[nom]), columns=onehot_enc.get_feature_names(nom), index=X.index)
        X = X.drop(nom, axis='columns')
        return pd.concat([X, df_onehot], axis='columns')
    def impute(self, X):
        ## 1. Numerical features
        X = X.fillna(X.median())

        ## 2. Categorical features
        X = X.fillna(X.mode().iloc[0])
        return X
    def process_num(self, data):
        return pd.DataFrame(StandardScaler().fit_transform(data), columns=data.columns, index=data.index)
    #########################################################
