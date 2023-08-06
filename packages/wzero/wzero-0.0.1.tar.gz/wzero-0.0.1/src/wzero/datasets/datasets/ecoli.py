import numpy as np
import pandas as pd
import os

from ..dataset import Dataset
from .. import utils

class Ecoli(Dataset):

    name = 'ecoli'
    reference_website = 'https://archive.ics.uci.edu/ml/datasets/ecoli'

    def __init__(self):
        super().__init__()
        
        if not self.name in self.downloaded_datasets:
            os.makedirs(self.download_folder, exist_ok=True)
            self.download()
        else:
            self.features = np.load(os.path.join(self.download_folder, 'features.npy'))
            self.labels = np.load(os.path.join(self.download_folder, 'labels.npy'))
            self.label_names = np.load(os.path.join(self.download_folder, 'label_names.npy'))

        self.splitted = False
        self.x_dim = (7,)
        self.y_dim = 8


    def download(self):

        data_path = utils.download_file('https://archive.ics.uci.edu/ml/machine-learning-databases/ecoli/ecoli.data', self.download_folder)
        data = pd.read_csv(data_path, header=None, delim_whitespace=True)
        
        self.features = data.iloc[:, 1:-1].values
        
        labels = data.iloc[:, -1]
        label_names = list(labels.unique())
        self.labels = labels.map(lambda x : label_names.index(x)).values
        self.label_names = np.array(label_names)

        os.remove(data_path)
        
        np.save(os.path.join(self.download_folder, 'features.npy'), self.features)
        np.save(os.path.join(self.download_folder, 'labels.npy'), self.labels)
        np.save(os.path.join(self.download_folder, 'label_names.npy'), self.label_names)