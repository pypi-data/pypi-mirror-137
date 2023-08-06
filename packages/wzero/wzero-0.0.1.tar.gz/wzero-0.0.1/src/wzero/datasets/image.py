# import numpy as np

# from .. import binarization

from .dataset import Dataset

class ImageDataset(Dataset):
    def __init__(self):
        super().__init__()
    
    def thermometer(self, nBits, **kwargs):
        _min = kwargs.get('min', 0)
        _max = kwargs.get('max', 255)
        return super().thermometer(nBits, _min, _max)