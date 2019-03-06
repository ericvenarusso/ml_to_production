from model import MachineLearning
from process import PreProcessing

class Main:
   
    def __init__(self):
        self.message = "Executando ..."
    
    def exec(self):
        print(self.message)
        PreProcessing().pipeline()
        model = MachineLearning().fit()
        MachineLearning().classify(model)

Main().exec()