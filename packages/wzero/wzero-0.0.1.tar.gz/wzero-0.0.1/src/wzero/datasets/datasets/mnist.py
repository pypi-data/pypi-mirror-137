import numpy as np
import os

from ..image import ImageDataset
from .. import utils

class Mnist(ImageDataset):
    
    name = 'mnist'
    reference_website='http://yann.lecun.com/exdb/mnist/'
    
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
        self.x_dim = np.array([28, 28])
        self.y_dim = 10

    def download(self):
        x_train_path = utils.download_file('http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz', self.download_folder)
        y_train_path = utils.download_file('http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz', self.download_folder)
        x_test_path = utils.download_file('http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz', self.download_folder)
        y_test_path = utils.download_file('http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz', self.download_folder)

        self.x_train = utils.load_ubyte(x_train_path, 60000, (28, 28))
        self.y_train = utils.load_ubyte(y_train_path, 60000, ())
        self.x_test = utils.load_ubyte(x_test_path, 10000, (28, 28))
        self.y_test = utils.load_ubyte(y_test_path, 10000, ())

        os.remove(x_train_path)
        os.remove(y_train_path)
        os.remove(x_test_path)
        os.remove(y_test_path)

        np.save(os.path.join(self.download_folder, 'x_train.npy'), self.x_train)
        np.save(os.path.join(self.download_folder, 'y_train.npy'), self.y_train)
        np.save(os.path.join(self.download_folder, 'x_test.npy'), self.x_test)
        np.save(os.path.join(self.download_folder, 'y_test.npy'), self.y_test)


        
    
