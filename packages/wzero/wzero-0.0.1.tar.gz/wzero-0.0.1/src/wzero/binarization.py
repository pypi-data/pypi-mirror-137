import numpy as np
from scipy.stats import norm

def threshold(x, th):
    return x > th

def one_hot(x, lenght=None):
    if lenght == None:
        lenght = x.max()+1
    oh = np.zeros([x.size, lenght])
    oh[np.arange(x.size), x] = 1
    return oh

def thermometer(x, nBits, min_, max_):
    t = (nBits + 1) * (x.astype(np.float32) - min_) / (max_ - min_)
    return np.stack([t > i for i in range(1, nBits+1)], axis=-1)

def bin_array(x, d):
    return np.fromstring(np.binary_repr(x, width=d), np.int8) - 48

def guassian_thermometer(x, nBits):
    norm_x = (x - x.mean()) / x.std()
    std_skws = norm.ppf(np.arange(1, nBits+1) / (nBits+1))
    terms = [norm_x > std_skw for std_skw in std_skws]
    return  np.stack(terms, axis=-1)

def get_splits(self, x, nBits, individual=False):
    data = np.sort(x.flatten()) if not individual else np.sort(x, axis=0)
    indicies = [int(data.shape[0]*i/(nBits+1)) for i in range(nBits+1)]
    return data[indicies][1:]
    

def distrib_therm(self, x, nBits=None, splits=None, individual=False):
    if splits == None:
        splits = get_splits(x, nBits, individual) 
    return np.stack([x > split for split in splits], axis=-1)