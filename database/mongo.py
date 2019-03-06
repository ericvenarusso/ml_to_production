import os
import csv
import json
import pymongo


class Mongo:
    
    def __init__(self):
        self.client = pymongo.MongoClient(os.environ["database_ip"], int(os.environ["database_port"]))
        self.db = self.client[os.environ["database_name"]]

    def find(self, collection, **kwargs):
        return [row for row in self.db[collection].find(kwargs)]

    def drop(self, collection):
        if collection in self.db.list_collection_names():
            self.db[collection].drop()

    def insert_one(self, collection, row):
        self.db[collection].insert_one(row)

    def insert_csv(self, csv_name, columns, collection):
        csv_file = open(f"{os.environ['csv_path']}{csv_name}", "r")
        csv_dict = csv.DictReader( csv_file )

        for each in csv_dict:
            row={}
            for field in columns:
                row[field]=each[field]

            self.db[collection].insert_one(each)