import numpy as np
from wnnc import CcRegressionWiSARD

class RegressionWiSARD:
    def __init__(self, num_inputs, tuple_lenght, num_classes, canonical=True):
        self.__num_inputs = num_inputs
        self.__tuple_lenght = tuple_lenght
        self.__num_classes = num_classes
        self.__canonical = canonical
        self.__model = CcRegressionWiSARD(num_inputs, tuple_lenght, num_classes, canonical)

    @property
    def num_inputs(self):
        return self.__num_inputs
    
    @property
    def tuple_lenght(self):
        return self.__tuple_lenght
    
    @property
    def num_classes(self):
        return self.__num_classes
    
    @property
    def canonical(self):
        return self.__canonical

    def train(self, x, y):
        self.__model.train(x, y)

    def predict(self, x):
        return self.__model.predict(x)
    
    def mental_images(self):
        return self.__model.mental_images()
    
    def get_size(self):
        return self.__model.get_size()