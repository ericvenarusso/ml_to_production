"""
    O Machine Learning to production tem como principal funcao "emular" como um grande projeto seria
    colocado em producao.

    Ele possue os seguintes componentes:

    process: Processamento dos dados.
    database: Configuracoes e ingestoes do Banco de Dados MongoDB.
    config: Possui arquivos shell que preparam o ambiente.
    model: Criacao do modelo de Machine Learning.
    api: Criacao de uma API a partir de um modelo ja treinado.
"""

from model import MachineLearning
from process import PreProcessing

class Main:


    def __init__(self):
        """
            Inicializa a variavel que sera utilizada para a execucao do arquivo.

            Exemplo:
                self.message: Recebe uma string com a messagem de execucacao
        """

        self.message = "Executando ..."
    
    def exec(self):
        """
            Proprosito
            ----------
            Executa todos os processos como: processamento dos dados, treinamento e 
            predicao de valores com Machine Learning.

            Parametros
            ----------
            none

            Retorno
            ----------
            none
        """
        print(self.message)
        PreProcessing().pipeline()
        model = MachineLearning().fit()
        MachineLearning().classify(model)


Main().exec()