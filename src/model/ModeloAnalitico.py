import time

from joblib import load, dump
from sklearn.base import BaseEstimator, ClassifierMixin
import pandas as pd

from src.common.app_common import path_app_model_generated

from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.decomposition import PCA

#
# Modelo de exemplo para classificar dígitos do dataset sklearn.datasets.load_digits()
# Um notebook de exeplo de treino pode ser verificado na pasta de _dev, derivado do
# site da sklearn https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html
#

class BaseModel(BaseEstimator, ClassifierMixin):

    def __init__(self, file_model=None, file_dataframe=None ):
        self.file_model = file_model
        self.file_dataframe = file_dataframe
        self.__model = make_pipeline(PCA(n_components=0.95),
                                     SVC(gamma=0.001))
                                     # Aqui o modelo pode ser inicializado por default,
                                     # ou pode ser completado apos processo de fit()
        self.__df = None
        if not (self.file_model is None): self.load_model()
        if not (self.file_dataframe is None): self.load_dataframe()

    def fit(self, X, y):
        self.__model.fit(X , y)
        # Este template não está preparado para treino
        # Um pipeline precisa ser criado aqui para completar a aplicação com treino
        return self

    def predict(self, X=None):
        if X is None: X = self.__df
        if X is None: raise Exception("Data Not Found")
        if not isinstance(X, pd.DataFrame):
            df_result = pd.DataFrame(self.__model.predict(X), columns=['predict'])
        else:
            df_result = pd.DataFrame(self.__model.predict(X),index=X.index, columns=['predict'])
        
        return df_result

    def pre_process(self, df):
        return df

    def load_model(self,file_model=None):
        if file_model is None:
            self.__model = load(open(self.file_model, 'rb'))
        else:
            self.__model = load(open(file_model, 'rb'))

    def load_dataframe(self,file_dataframe=None):
        if file_dataframe is None:
            # Primeiro coluna sempre é um índice.
            df = pd.read_csv(self.file_dataframe, index_col=0)
            self.__df = self.pre_process(df)
        else:
            # Primeiro coluna sempre é um índice.
            df = pd.read_csv(file_dataframe, index_col=0)
            self.__df = self.pre_process(df)
        
        return self.__df

    def save_model(self):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        filename = path_app_model_generated + "/app_base_model_v" + '_' + timestr + '.joblib'
        f = open(filename, 'wb')
        dump(self.__model, f, compress=3)
        f.close()
