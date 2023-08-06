import numpy as np
import pandas as pd
import os

from ..dataset import Dataset
from .. import utils

class Glass(Dataset):

    name = 'glass'
    reference_website = 'https://archive.ics.uci.edu/ml/datasets/glass+identification'

    def __init__(self):
        super().__init__()
        
        if not self.name in self.downloaded_datasets:
            os.makedirs(self.download_folder, exist_ok=True)
            self.download()
        else:
            self.features = np.load(os.path.join(self.download_folder, 'features.npy'))
            self.labels = np.load(os.path.join(self.download_folder, 'labels.npy'))

        self.splitted = False
        self.x_dim = (9,)
        self.y_dim = 6


    def download(self):

        data_path = utils.download_file('https://archive.ics.uci.edu/ml/machine-learning-databases/glass/glass.data', self.download_folder)
        data = pd.read_csv(data_path, header=None)
        
        self.features = data.iloc[:, 1:-1].values
        
        labels = data.iloc[:, -1]
        label_names = list(labels.unique())
        self.labels = labels.map(lambda x : label_names.index(x)).values

        os.remove(data_path)
        
        np.save(os.path.join(self.download_folder, 'features.npy'), self.features)
        np.save(os.path.join(self.download_folder, 'labels.npy'), self.labels)