from sklearn.preprocessing import MinMaxScaler
from database.mongo        import Mongo
import pandas as pd
import os

class PreProcessing:


    def __init__(self):
        """
            Inicializa variaveis que serao utilizadas no PreProcessamento.

            Exemplo:
                self.train: Registros da collection train
                self.test: Registros da collection test
                self.dict_map: Registro da collection dict_map
        """

        self.train = pd.DataFrame(Mongo().find("train"))
        self.test  = pd.DataFrame(Mongo().find("test"))
        self.dict_map = Mongo().find("target_map")

    def pipeline(self):
        """
            Proprosito
            ----------
            Execucao das funcoes sequencialmente que farao o preprocessamento.
            dos dados. 

            Parametros
            ----------
            none

            Retorno
            ----------
            none
        """

        self.float_transform("bone_length", "rotting_flesh", "hair_length", "has_soul")
        self.minmaxscaler_transform("bone_length", "rotting_flesh", "hair_length", "has_soul")
        self.dummies_transform("color")
        self.target_map()
        self.save_result("result")

    def float_transform(self, *args):
        """
            Proprosito
            ----------
            Transformacao dos dados para float.

            Parametros
            ----------
            args: colunas a serem parseadas

            Retorno
            ----------
            none
        """

        for column in args:
            self.train[column] = self.train[column].apply(lambda x:float(x))
            self.test[column]  = self.test[column].apply(lambda x:float(x))
 
    def minmaxscaler_transform(self, *args):
        """
            Proprosito
            ----------
            Transformacao dos dados com o MinMaxScaler.

            Parametros
            ----------
            args: colunas a serem parseadas

            Retorno
            ----------
            none
        """

        self.train[list(args)] = MinMaxScaler().fit_transform(self.train[list(args)])
        self.test[list(args)]  = MinMaxScaler().fit_transform(self.test[list(args)])

    def dummies_transform(self, *args):
        """
            Proprosito
            ----------
            Transformacao das colunas para variaveis dummies.

            Parametros
            ----------
            args: colunas a serem parseadas

            Retorno
            ----------
            none
        """

        self.train = pd.get_dummies(self.train, columns = list(args), drop_first = True)
        self.test  = pd.get_dummies(self.test, columns  = list(args), drop_first = True)

    def target_map(self, invert = False, dataframe = pd.DataFrame()):
        """
            Proprosito
            ----------
            Mapeamento da coluna target para binario.

            Parametros
            ----------
            invert: se o dicionario deve ser inverso
            dataframe: DataFrame a ser mapeado

            Retorno
            ----------
            dataframe: DataFrame mapeado
        """

        if invert:
            inv_map = {v: k for k, v in self.dict_map[0].items()}
            dataframe["type"] = dataframe["type"].apply(lambda x: inv_map[x])
            return dataframe
        else:
            self.train["type"] = self.train["type"].apply(lambda x: self.dict_map[0][x])

    def save_result(self, path):
        """
            Proprosito
            ----------
            Salva os DataFrames em um objeto Pickle

            Parametros
            ----------
            invert: caminho onde devera ser salvo o objeto Pickle.

            Retorno
            ----------
            none
        """

        self.train.to_pickle(f"{os.environ['dataframe_result_path']}/train.pkl")
        self.test.to_pickle(f"{os.environ['dataframe_result_path']}/test.pkl")
