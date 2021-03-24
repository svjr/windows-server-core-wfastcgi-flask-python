from datetime import time

from joblib import load, dump
from sklearn.base import BaseEstimator, ClassifierMixin
import pandas as pd

from src.common.app_common import name_folder_generated


class BaseModel(BaseEstimator, ClassifierMixin):

    def __init__(self, file_model=None, file_dataframe=None, ):
        self.__model = None  # Aqui o modelo pode ser inicializado por default
        self.__df = None
        self.__file_model = file_model
        self.__file_dataframe = file_dataframe
        if not (self.__file_model is None): self.load_model()
        if not (self.__file_dataframe is None): self.load_dataframe()

    def fit(self, X, y):
        self.__model.fit(X, y)
        # Este template não está preparado para treino
        # Um pipeline precisa ser criado aqui para completar a aplicação com treino
        return self

    def predict(self, X=None):
        if X is None: X = self.__df
        if X is None: raise Exception("Data Not Found")
        if not isinstance(X, pd.DataFrame):
            return self.__model.predict(X)
        else:
            df_result = pd.DataFrame(self.__model.predict(X),index=X.index, columns=['predict'])
            return df_result

    def pre_process(self, df):
        return df

    def load_model(self):
        self.__model = load(open(self.__file_model, 'rb'))

    def load_dataframe(self):
        # Primeiro coluna sempre é um índice.
        df = pd.read_csv(self.__file_dataframe, index_col=0)
        self.__df = self.pre_process(df)
        return self.__df

    def save_model(self):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        filename = name_folder_generated + "/app_base_model_v" + '_' + timestr + '.joblib'
        f = open(filename, 'wb')
        dump(self.__model, f, compress=3)
        f.close()
