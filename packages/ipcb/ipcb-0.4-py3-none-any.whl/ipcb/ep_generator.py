import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import cv2
import tensorflow as tf


def get_dataset(RUN_FOLDER):
    '''
    input: dataset path. One inner fold per class (2)
           Ex: ".../dataset/"
    outputs: image arrays separated per class
           Ex: class_1.shape = (K, 1, height, width, channels)
               class_2.shape = (K, 1, height, width, channels)
               
               Where K is the number of samples per class in the dataset
    '''
    # get image paths
    anom_path = os.path.join(RUN_FOLDER, 'anom')
    good_path = os.path.join(RUN_FOLDER, 'good')
    
    anom_np = np.array(glob.glob(anom_path + '/*.jpg'))
    good_np = np.array(glob.glob(good_path + '/*.jpg'))
    
    # shuffle indices
    anom_idx = np.arange(anom_np.shape[0])
    good_idx = np.arange(good_np.shape[0])    
    np.random.shuffle(anom_idx)   
    np.random.shuffle(good_idx)    
    anom_np = anom_np[anom_idx]
    good_np = good_np[good_idx]    
    
    # save image arrays into memmory
    anom_array = []
    good_array = []
    for anom_path in anom_np:        
        anom = cv2.imread(anom_path).astype(np.float16)
        anom_array.append(anom / 255) # rescale [0-255, 0-1]
        
    for good_path in good_np:        
        good = cv2.imread(good_path).astype(np.float16)
        good_array.append(good / 255)
    
    anom_array = np.array(anom_array)
    good_array = np.array(good_array)
    
    size = anom_array.shape[1:]

    anom_array = anom_array.reshape(-1, 1, size[0], size[1], size[2])
    good_array = good_array.reshape(-1, 1, size[0], size[1], size[2])
       
    return anom_array, good_array


def gen_episode(data, anom_shots=2, good_shots=2, query_shots=4, batch_size=1):
    """
    take the dataset as input and outputs a few-shot batch episode
    inputs:
        anom_shots  -> number of anomaly shots
        good_shots  -> number of template shots
        query_shots -> number of test shots
    outputs:
        train_batch -> a list with all inputs in order and batched
        labels -> the respective training labels of this episode
    """
    anom_idx  = np.arange(data[0].shape[0])
    good_idx  = np.arange(data[1].shape[0])     

    H = data[0].shape[2]
    W = data[0].shape[3]
    C = data[0].shape[4]   
    
    anom_batch  = []
    good_batch  = []
    query_batch = []
    labels      = []
    train_batch = []

    for i in range(batch_size):
        
        query_class = np.random.randint(0, 2) # random class for the query         
        
        # anom batch - class 0
        anom_shots_idx = np.random.choice(anom_idx, anom_shots, replace=False)
        sample_anom_shots = data[0][anom_shots_idx].reshape((-1, H, W, C))
        anom_label = 0
        # good batch - class 1
        good_shots_idx = np.random.choice(good_idx, good_shots, replace=False)
        sample_good_shots = data[1][good_shots_idx].reshape((-1, H, W, C))
        good_label = 1
        
    
        # query batch
        anom_query_shots = query_shots // 2 # number of query shots separated for anomalies
        good_query_shots = query_shots - anom_query_shots
        
        # do not take queries that are equal to some of the support set images
        anom_query_idx = np.delete(anom_idx, anom_shots_idx)
        good_query_idx = np.delete(good_idx, good_shots_idx)
        
        anom_query_idx = np.random.choice(anom_query_idx, anom_query_shots)
        good_query_idx = np.random.choice(good_query_idx, good_query_shots)
        
        
        sample_query_shots = np.concatenate([data[0][anom_query_idx],
                                             data[1][good_query_idx]])
        query_label = np.concatenate([np.zeros(anom_query_shots),
                                      np.ones(good_query_shots)])
        
        query_idx = np.arange(sample_query_shots.shape[0])
        np.random.shuffle(query_idx)
        sample_query_shots = sample_query_shots[query_idx].reshape(-1, *sample_query_shots.shape[-3:])
        query_label = query_label[query_idx]
        
        
        # generate episode labels
        label_1 = np.array((anom_label == query_label) * 1)
        label_2 = np.array((good_label == query_label) * 1)
        ep_label = np.column_stack([label_1, label_2])
                
        # few-shot batches
        anom_batch.append(sample_anom_shots)
        good_batch.append(sample_good_shots)
        query_batch.append(sample_query_shots)
        labels.append(ep_label)
            
    # organize each few-shot batch into a single array of shape == (shots, batch_size, *img.shape)
    train_batch = []
    for i in range(anom_shots):
        train_batch.append(np.array(anom_batch)[:, i])
    for i in range(good_shots):
        train_batch.append(np.array(good_batch)[:, i])
    for i in range(query_shots):
        train_batch.append(np.array(query_batch)[:, i])
    
    # organize batch label
    labels = np.array(labels)
    labels = labels.reshape((-1, *labels.shape[1:]))
        
    return train_batch, labels