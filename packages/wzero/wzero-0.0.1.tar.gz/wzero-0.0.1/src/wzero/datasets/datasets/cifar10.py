import numpy as np
import os
import shutil
import pickle

from ..image_rgb import ImageDatasetRGB
from .. import utils

class Cifar10(ImageDatasetRGB):
    
    name = 'cifar10'
    reference_website = 'https://www.cs.toronto.edu/~kriz/cifar.html'
    
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
            self.label_names = np.load(os.path.join(self.download_folder, 'label_names.npy'))
        
        self.splitted = True
        self.x_dim = np.array([32, 32, 3])
        self.y_dim = 10

    def download(self):
        
        filepath =  utils.download_file('https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz', self.download_folder)
        shutil.unpack_archive(filepath)
        os.remove(filepath)

        self.x_train = np.empty((50000, 32, 32, 3), dtype=np.uint8)
        self.y_train = np.empty(50000, dtype=np.int32)

        folder = 'cifar-10-batches-py'
        num_batches = 5
        batch_size = 10000

        for i in range(num_batches):
            with open(os.path.join(folder, f'data_batch_{i+1}'), 'rb') as f:
                data = pickle.load(f, encoding='bytes')
            self.x_train[i*batch_size:(i+1)*batch_size] = data[b'data'].reshape(10000, 3, 32, 32).transpose(0, 2, 3, 1)
            self.y_train[i*batch_size:(i+1)*batch_size] = data[b'labels']

        with open(os.path.join(folder, 'test_batch'), 'rb') as f:
            data = pickle.load(f, encoding='bytes')
        self.x_test = data[b'data'].reshape(10000, 3, 32, 32).transpose(0, 2, 3, 1)
        self.y_test = np.array(data[b'labels'])

        with open(os.path.join(folder, 'batches.meta'), 'rb') as f:
            meta = pickle.load(f)
        self.label_names = np.array(meta['label_names'])

        shutil.rmtree(folder)

        np.save(os.path.join(self.download_folder, 'x_train.npy'), self.x_train)
        np.save(os.path.join(self.download_folder, 'y_train.npy'), self.y_train)
        np.save(os.path.join(self.download_folder, 'x_test.npy'), self.x_test)
        np.save(os.path.join(self.download_folder, 'y_test.npy'), self.y_test)
        np.save(os.path.join(self.download_folder, 'label_names.npy'), self.label_names)
    
