from flask_restful import reqparse, abort, Api, Resource
from flask         import Flask
from glob          import glob
import numpy as np
import pickle
import os

"""
    Criacao de uma API a partir de um modelo de Machine Learning ja
    treinado.
"""

app = Flask(__name__)
api = Api(app)

"""
    Faz a leitura do ultimo modelo
"""

clf_path = max(glob(f"{os.environ['model_path']}*.pkl"), key = os.path.getctime)

with open(clf_path, "rb") as f:
    clf = pickle.load(f)

"""
    Adicao de argumentos na API
"""

parser = reqparse.RequestParser()
parser.add_argument("id", type = int, required = True)
parser.add_argument("list", type = str, required = True)

class ClassifyMonsters(Resource):

    def get(self):
        """
            Proprosito
            ----------
            Retornar a resposta do predict do Machine Learning

            Parametros
            ----------
            none

            Retorno
            ----------
            none
        """

        args = parser.parse_args()
        user_id = args["id"]
        user_list = np.asarray([float(string) for string in args["list"].split(",")]).reshape(1, -1)
        target_map = {0 : "Ghoul", 1 : "Goblin" ,  2 : "Goblin"}
        prediction = target_map[clf.predict(user_list).tolist()[0]]
        return {"id": user_id, "prediction": prediction}

api.add_resource(ClassifyMonsters, "/classify")

if __name__ == '__main__':
    app.run(debug = True)