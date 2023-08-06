import numpy as np
import pandas as pd
import os

from ..dataset import Dataset
from .. import utils

class Segment(Dataset):

    name = 'segment'
    reference_website = 'https://archive.ics.uci.edu/ml/datasets/image+segmentation'

    def __init__(self):
        super().__init__()
        
        if not self.name in self.downloaded_datasets:
            os.makedirs(self.download_folder, exist_ok=True)
            self.download()
        else:
            self.x_train = np.load(os.path.join(self.download_folder, 'x_train.npy'))
            self.y_train = np.load(os.path.join(self.download_folder, 'y_train.npy'))
            self.x_test = np.load(os.path.join(self.download_folder, 'x_test.npy'))
            self.y_test = np.load(os.path.join(self.download_folder, 'y_test.npy'))

        self.splitted = True
        self.x_dim = (19,)
        self.y_dim = 7


    def download(self):

        train_path = utils.download_file('https://archive.ics.uci.edu/ml/machine-learning-databases/image/segmentation.data', self.download_folder)
        data = pd.read_csv(train_path, comment=';')
        
        self.x_train = data.values
        
        labels = data.index
        label_names = list(labels.unique())
        self.y_train = labels.map(lambda x : label_names.index(x)).values

        os.remove(train_path)

        test_path = utils.download_file('https://archive.ics.uci.edu/ml/machine-learning-databases/image/segmentation.test', self.download_folder)
        data = pd.read_csv(test_path, comment=';')

        self.x_test = data.values
        
        labels = data.index
        self.y_test = labels.map(lambda x : label_names.index(x)).values

        os.remove(test_path)
        
        np.save(os.path.join(self.download_folder, 'x_train.npy'), self.x_train)
        np.save(os.path.join(self.download_folder, 'y_train.npy'), self.y_train)
        np.save(os.path.join(self.download_folder, 'x_test.npy'), self.x_test)
        np.save(os.path.join(self.download_folder, 'y_test.npy'), self.y_test)