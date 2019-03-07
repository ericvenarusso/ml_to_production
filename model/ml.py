from process.preprocessing import PreProcessing
from database.mongo        import Mongo
from sklearn.svm           import SVC
from datetime              import datetime
import pandas as pd
import pickle
import json
import os

class MachineLearning:

    def __init__(self):
        """
            Inicializa variaveis que serao utilizadas no Machine Learning.

            Exemplo:
                self.train: Registros do objeto Pickle train
                self.test: Registros do objeto Pickle test
                self.model: Modelo de Classificacao SVC
                self.data: Data atual
                self.X_columns: Lista de colunas para o DataFrame X
                self.y_columns: Lista de colunas para o DataFrame y
                self.model_name: Nome do Modelo
        """

        self.train = pd.read_pickle(f"{os.environ['dataframe_result_path']}/train.pkl")
        self.test  = pd.read_pickle(f"{os.environ['dataframe_result_path']}/test.pkl")
        self.model = SVC(C = 1, degree = 2, gamma = "auto", kernel = "rbf")
        self.date  = datetime.now().strftime("%m-%d-%YT%H:%M:%S")
        self.X_columns = ["bone_length", "hair_length", "has_soul", "rotting_flesh", "color_blood", "color_blue", "color_clear", "color_green", "color_white"]
        self.y_columns = "type"
        self.model_name = f"model_{self.date}.pkl"
        

    def fit(self):
        """
            Proprosito
            ----------
            Fazer o treinamento do modelo

            Parametros
            ----------
            none

            Retorno
            ----------
            none
        """

        X = self.train[self.X_columns]
        y = self.train[self.y_columns]
        fitted_model = self.model.fit(X, y)
        
        self.save_model(fitted_model)
        
        return fitted_model

    def save_model(self, model):
        """
            Proprosito
            ----------
            Salvar o modelo treinado e fazer a insercao dos parametros no MongoDB

            Parametros
            ----------
            model: Modelo treinado

            Retorno
            ----------
            none
        """

        models_params = {
                            "name": self.model_name,
                            "X":  self.X_columns,
                            "y": self.y_columns,
                            "params": model.get_params()
                        }

        Mongo().insert_one("models", models_params)
        pickle.dump(self.model, open(f"{os.environ['model_path']}{self.model_name}", "wb"))

    def classify(self, model):
        """
            Proprosito
            ----------
            Faz a classificacao dos registros e salva o resultado no MongoDB

            Parametros
            ----------
            model: Modelo treinado

            Retorno
            ----------
            none
        """

        X = self.test[self.X_columns]
        y_pred = model.predict(X)

        pred = pd.DataFrame({'id': self.test['id'], 'type': y_pred})

        mapped_pred = PreProcessing().target_map(dataframe = pred, invert = True)

        result = {
                "model_name": self.model_name,
                "predict_results": list(json.loads(mapped_pred.T.to_json()).values())
              }
        
        Mongo().insert_one("results", result)
              