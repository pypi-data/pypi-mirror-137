import numpy as np

from . import metrics
from . import utils
from . import models

def profile(model, dataset, predict_args=[]):
    
    data = {}

    data['train_time'], null = utils.timeit(model.train, dataset.x_train, dataset.y_train)
    data['test_time'], predictions = utils.timeit(model.predict, dataset.x_test, *predict_args)
    data['accuracy'] = metrics.accuracy(dataset.y_test, predictions)
    
    return data

def mean_profile(model_gen, dataset, n=1, raw=False, predict_args=[]):
    
    data = {
        'train_time': np.empty(n),
        'test_time': np.empty(n),
        'accuracy': np.empty(n)
    }

    for i in range(n):

        model = model_gen()

        data['train_time'][i], null = utils.timeit(model.train, dataset.x_train, dataset.y_train)
        data['test_time'][i], predictions = utils.timeit(model.predict, dataset.x_test, *predict_args)
        data['accuracy'][i] = metrics.accuracy(dataset.y_test, predictions)
    
    if raw:
        return data
    
    data['train_time'], data['train_time_std'] = data['train_time'].mean(), data['train_time'].std()
    data['test_time'], data['test_time_std'] = data['test_time'].mean(), data['test_time'].std()
    data['accuracy'], data['accuracy_std'] = data['accuracy'].mean(), data['accuracy'].std()

    return data