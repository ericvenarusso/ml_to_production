from sklearn.preprocessing import MinMaxScaler
from database.mongo        import Mongo
import pandas as pd
import os

class PreProcessing:


    def __init__(self):
        self.train = pd.DataFrame(Mongo().find("train"))
        self.test  = pd.DataFrame(Mongo().find("test"))
        self.dict_map = Mongo().find("target_map")

    def pipeline(self):
        self.float_transform("bone_length", "rotting_flesh", "hair_length", "has_soul")
        self.minmaxscaler_transform("bone_length", "rotting_flesh", "hair_length", "has_soul")
        self.dummies_transform("color")
        self.target_map()
        self.save_result("result")

    def float_transform(self, *args):
        for column in args:
            self.train[column] = self.train[column].apply(lambda x:float(x))
            self.test[column]  = self.test[column].apply(lambda x:float(x))
 
    def minmaxscaler_transform(self, *args):
        self.train[list(args)] = MinMaxScaler().fit_transform(self.train[list(args)])
        self.test[list(args)]  = MinMaxScaler().fit_transform(self.test[list(args)])

    def dummies_transform(self, *args):
        self.train = pd.get_dummies(self.train, columns = list(args), drop_first = True)
        self.test  = pd.get_dummies(self.test, columns  = list(args), drop_first = True)

    def target_map(self, invert = False, dataframe = pd.DataFrame()):
        if invert:
            inv_map = {v: k for k, v in self.dict_map[0].items()}
            dataframe["type"] = dataframe["type"].apply(lambda x: inv_map[x])
            return dataframe
        else:
            self.train["type"] = self.train["type"].apply(lambda x: self.dict_map[0][x])

    def save_result(self, path):
        self.train.to_pickle(f"{os.environ['dataframe_result_path']}/train.pkl")
        self.test.to_pickle(f"{os.environ['dataframe_result_path']}/test.pkl")
