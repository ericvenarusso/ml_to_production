import os
import csv
import json
import pymongo


class Mongo:
    

    def __init__(self):
        """
            Inicializa variaveis que serao utilizadas para funcoes do MongoDB.

            Exemplo:
                self.client: Configuracoes do Banco de Dados
                self.db: Aponta para o Banco de dados
        """

        self.client = pymongo.MongoClient(os.environ["database_ip"], int(os.environ["database_port"]))
        self.db = self.client[os.environ["database_name"]]

    def find(self, collection, **kwargs):
        """
            Proprosito
            ----------
            Executar a funcao find do MongoDB

            Parametros
            ----------
            collection: Nome da Collection
            kargs: Argumentos da funcao find

            Retorno
            ----------
            parsed_df: Registros gerados pela consulta
        """

        return [row for row in self.db[collection].find(kwargs)]

    def drop(self, collection):
        """
            Proprosito
            ----------
            Caso a Collection exista executar a funcao drop do MongoDB

            Parametros
            ----------
            collection: Nome da Collection

            Retorno
            ----------
            none
        """

        if collection in self.db.list_collection_names():
            self.db[collection].drop()

    def insert_one(self, collection, row):
        """
            Proprosito
            ----------
            Executar a funcao insert_one do MongoDB

            Parametros
            ----------
            collection: Nome da Collection
            row: Linha que sera inserida

            Retorno
            ----------
            none
        """

        self.db[collection].insert_one(row)

    def insert_csv(self, csv_name, columns, collection):
        """
            Proprosito
            ----------
            Fazer a injestao de um csv no MongoDB

            Parametros
            ----------
            csv_name: Nome do csv
            columns: Colunas do csv
            collection: Nome da Collection

            Retorno
            ----------
            none
        """

        csv_file = open(f"{os.environ['csv_path']}{csv_name}", "r")
        csv_dict = csv.DictReader( csv_file )

        for each in csv_dict:
            row={}
            for field in columns:
                row[field]=each[field]

            self.db[collection].insert_one(each)