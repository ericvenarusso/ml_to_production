
import pickle
from flask import Flask
import numpy as np
import pdb
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

clf_path = '/home/ericvenarusso/workspace/monsters/model/result/model_03-06-2019T15:47:39.pkl'

with open(clf_path, 'rb') as f:
    clf = pickle.load(f)

parser = reqparse.RequestParser()
parser.add_argument('id', type = int, required = True)
parser.add_argument('list', type = str, required = True)

class ClassifyMonsters(Resource):

    def get(self):
        args = parser.parse_args()
        user_id = args['id']
        user_list = np.asarray([float(string) for string in args['list'].split(",")]).reshape(1, -1)
        target_map = {0 : "Ghoul", 1 : "Goblin" ,  2 : "Goblin"}
        prediction = target_map[clf.predict(user_list).tolist()[0]]
        return {'id': user_id, 'prediction': prediction}

api.add_resource(ClassifyMonsters, '/classify')

if __name__ == '__main__':
    app.run(debug = True)