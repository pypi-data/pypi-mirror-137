import numpy as np
from pathlib import Path
import os

from .. import binarization

class Dataset:
    def __init__(self):
        self.main_download_folder = os.path.join(Path.home(), 'wnn_datasets')
        os.makedirs(self.main_download_folder, exist_ok=True)
        self.downloaded_datasets = os.listdir(self.main_download_folder)
        self.download_folder = os.path.join(self.main_download_folder, self.name) # downlaod folder of the child dataset; self.name -> static attribute of child dataset

    def flatten(self):
        
        if self.splitted:
            self.x_train = self.x_train.reshape(-1, self.x_dim.prod())
            self.x_test = self.x_test.reshape(-1, self.x_dim.prod())
            self.x_dim = np.array(self.x_train.shape[1:])
        else:
            self.features = self.features.reshape(-1, self.x_dim.prod())
            self.x_dim = np.array(self.features.shape[1:])
        
        return self
    
    def shuffle(self, seed=None):

        if seed != None:
            np.random.seed(seed)
        
        indexs = np.arange(self.features.shape[0])
        np.random.shuffle(indexs)
        
        if self.splitted:
            self.x_train = self.x_train[indexs]
            self.y_train = self.y_train[indexs]
            self.x_test = self.x_test[indexs]
            self.y_test = self.y_test[indexs]
        else:
            self.features = self.features[indexs]
            self.labels = self.labels[indexs]
        
        return self
    
    def train_test_split(self, train_size=0.8, shuffle=True, seed=None):
        
        if self.splitted:
            return self
        
        if shuffle:
            self.shuffle(seed)

        split_index = int(self.features.shape[0] * train_size)

        self.x_train = self.features[:split_index]
        self.y_train = self.labels[:split_index]
        self.x_test = self.features[split_index:]
        self.y_test = self.labels[split_index:]

        self.features = None
        self.labels = None

        self.splitted = True

        return self
    
    def threshold(self, t):
        if self.splitted:
            self.x_train = (self.x_train > t)
            self.x_test = (self.x_test > t)
        else:
            self.features = (self.features > t)
        return self

    def thermometer(self, nBits, min_=None, max_=None):
        if self.splitted: 
            min_ = self.x_train.min(axis=0) if min_ == None else min_
            max_ = self.x_train.max(axis=0) if max_ == None else max_
            self.x_train = binarization.thermometer(self.x_train, nBits, min_, max_)
            self.x_test = binarization.thermometer(self.x_test, nBits, min_, max_)
            self.x_dim = np.array(self.x_train.shape[1:])
        else:
            min_ = self.features.min(axis=0) if min_ == None else min_
            max_ = self.features.max(axis=0) if max_ == None else max_
            self.features = binarization.thermometer(self.features, nBits, min_, max_)
            self.x_dim = np.array(self.features.shape[1:])
            
        return self
    
    def distrib_term(self, nBits, individual=False):
        if self.splitted:
            splits = binarization.get_splits(self.x_train, nBits, individual)
            self.x_train = binarization.distrib_therm(self.x_train, splits=splits)
            self.x_test = binarization.distrib_therm(self.x_test, splits=splits)
            self.x_dim = np.array(self.x_train.shape[1:])
        else:
            self.features = binarization.distrib_therm(self.features, nBits, individual=individual)
            self.x_dim = np.array(self.features.shape[1:])
        
        return self

    def guassian_thermometer(self, nBits):
        if self.splitted: 
            self.x_train = binarization.guassian_thermometer(self.x_train, nBits)
            self.x_test = binarization.guassian_thermometer(self.x_test, nBits)
            self.x_dim = np.array(self.x_train.shape[1:])
        else:
            self.data = binarization.guassian_thermometer(self.data, nBits)
            self.x_dim = np.array(self.features.shape[1:])
        return self
    
    def label_distribution(self):

        train_dist = np.array([(self.y_train == i).sum() for i in range(self.y_dim)])
        train_dist = train_dist / train_dist.sum()

        test_dist = np.array([(self.y_test == i).sum() for i in range(self.y_dim)])
        test_dist = test_dist / test_dist.sum()

        data = {
            'train': train_dist,
            'test': test_dist
        }
        
        return data
    
    def get_info(self):
        if self.info:
            print(self.info) 


