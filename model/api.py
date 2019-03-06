import pickle
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

clf_path = '/home/ericvenarusso/workspace/monsters/model/result/model_03-06-2019T15:47:39.pkl'

with open(clf_path, 'rb') as f:
    clf = pickle.load(f)

parser = reqparse.RequestParser()
parser.add_argument('query')

class ClassifyMonsters(Resource):

    def get(self):
        
        args = parser.parse_args()
        user_query = args['query']
        
        prediction = clf.predict(user_query)
        
        return {'prediction': prediction}

api.add_resource(ClassifyMonsters, '/')

if __name__ == '__main__':
    app.run(debug = True)