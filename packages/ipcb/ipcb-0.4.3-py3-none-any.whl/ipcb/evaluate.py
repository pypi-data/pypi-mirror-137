# import tensorflow as tf
# import logging
# tf.get_logger().setLevel(logging.ERROR)
# tf.autograph.set_verbosity(0)

# import cv2
# import numpy as np
# import os
# import glob
# import time
# import pydot
# import matplotlib.pyplot as plt
# from tqdm.notebook import tqdm, trange

# from tensorflow.keras import backend as K
# from tensorflow.keras.datasets import mnist
# from tensorflow.keras.models import Model, Sequential, load_model
# from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, GlobalAveragePooling2D, Conv2DTranspose, BatchNormalization, Dropout, Flatten, Input, Reshape, Lambda, Concatenate, Add
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.losses import mse, binary_crossentropy
# from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.utils import plot_model

# import scripts.episode_generator_v3 as epgen
# import scripts.resultsData as results

# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#   try:
#     tf.config.experimental.set_virtual_device_configuration(gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=6000)])
#   except RuntimeError as e:
#     print(e)

# # tf.compat.v1.disable_eager_execution()
# gpus

# def load_data(train_path, test_path):
    
#     # main = 'D:/Documentos/#DATASETS/deepPCB_custom/custom/50'
#     # code = 'S_160-OL_0.25-AoI_1.0'
    
#     np.random.seed(42)

#     train_temps, train_tests = epgen.get_dataset(train_path)
#     val_temps, val_tests = epgen.get_dataset(test_path)

#     test_set, _ = epgen.train_test_split(val_temps, val_tests, 1) # static test data with 60% of default dataset
#     train_set, _ = epgen.train_test_split(train_temps, train_tests, 1)
#     _ = 0


#     print("train TEMPS data size:", train_set[0].shape)
#     print("train TESTS data size:", train_set[1].shape)

#     print("\nval TEMPS data size:", test_set[0].shape)
#     print("val TESTS data size:", test_set[1].shape)
    
#     return train_set, test_set


# def evaluate(model_path, data, batch_size, iterations):
#     """
#     The model should receive a RANDOM BATCH of generated episodes from
#     data that it has NEVER SEEN BEFORE. The results will be rounded to 
#     the closest integer (0 or 1) and finally compared to the ground 
#     truth labels. The acc will be the mean from all returned iterations.
#     inputs:
#         model_path: .h5py model file path
#         data: output tuple taken from "epg.get_dataset()" -> (2, n, 1, height, width, channels)
#         batch_size: number of inputs passed simultaneously to the model 
#         iterations: number of random repetitions to the model be tested.
#     """
    
#     model = load_model(model_path)
#     model.compile(Adam())
#     acc_log = []
#     for i in range(iterations):
        
#         batch, label = epgen.get_episode(data, batch_size)

#         y_pred = np.round(model.predict(batch))

#         acc = np.mean(y_pred == label)
#         acc_log.append(acc)
    
#     mean_acc = np.round(np.mean(np.array(acc_log)) * 100, 3)
#     plot = plot_model(model, show_shapes=True, expand_nested=True)
    
#     return plot, mean_acc


# def evaluate_debug(model_path, data, batch_size, iterations):
#     """
#     The model should receive a RANDOM BATCH of generated episodes from
#     data that it has NEVER SEEN BEFORE. The results will be rounded to 
#     the closest integer (0 or 1) and finally compared to the ground 
#     truth labels. The acc will be the mean from all returned iterations.
#     inputs:
#         model_path: .h5py model file path
#         data: output tuple taken from "epg.get_dataset()" -> (2, n, 1, height, width, channels)
#         batch_size: number of inputs passed simultaneously to the model 
#         iterations: number of random repetitions to the model be tested.
#     """
    
#     model = load_model(model_path)
#     model.compile(Adam())
#     acc_log = []
#     for i in range(iterations):
        
#         batch, label = epgen.get_episode(data, batch_size)   

#         y_pred = np.round(model.predict(batch))
        
#         misses = np.argmin(y_pred == label)
        
#         if misses:
#             return batch, label, y_pred


# def evaluate_fewshot(model_path, data, batch_size, iterations, k, q):
#     """
#     The model should receive a RANDOM BATCH of generated episodes from
#     data that it has NEVER SEEN BEFORE. The results will be rounded to 
#     the closest integer (0 or 1) and finally compared to the ground 
#     truth labels. The acc will be the mean from all returned iterations.
#     inputs:
#         model_path: .h5py model file path
#         data: output tuple taken from "epg.get_dataset()" -> (2, n, 1, height, width, channels)
#         batch_size: number of inputs passed simultaneously to the model 
#         iterations: number of random repetitions to the model be tested.
#     """
    
#     model = load_model(model_path)
#     model.compile(Adam())
#     acc_log = []
#     for i in trange(iterations):
        
#         batch, label = epgen.get_episode_few_shot(data, k, q, batch_size)

#         y_pred = np.round(model.predict(batch))

#         acc = np.mean(y_pred == label)
#         acc_log.append(acc)
    
#     mean_acc = np.round(np.mean(np.array(acc_log)) * 100, 3)
#     plot = plot_model(model, show_shapes=True, expand_nested=True)
    
#     return plot, mean_acc


# def evaluate_fewshot_2S(model, data, batch_size, iterations, k, q):
#     """
#     The model should receive a RANDOM BATCH of generated episodes from
#     data that it has NEVER SEEN BEFORE. The results will be rounded to 
#     the closest integer (0 or 1) and finally compared to the ground 
#     truth labels. The acc will be the mean from all returned iterations.
#     inputs:
#         model_path: .h5py model file path
#         data: output tuple taken from "epg.get_dataset()" -> (2, n, 1, height, width, channels)
#         batch_size: number of inputs passed simultaneously to the model 
#         iterations: number of random repetitions to the model be tested.
#     """

#     model.compile(Adam())
#     acc_log = []
#     for i in trange(iterations):
        
#         batch, label = epgen.get_episode_few_shot_2S(data, k, q, batch_size)
#         label = np.argmax(label, axis=1)
        
#         logits = model.predict(batch)
#         y_pred = np.argmax(logits, axis=1)

#         acc = np.mean(y_pred == label)
#         acc_log.append(acc)
    
#     mean_acc = np.round(np.mean(np.array(acc_log)) * 100, 3)
#     plot = plot_model(model, show_shapes=True, expand_nested=True)
    
#     return plot, mean_acc


# def validate(model, data, batch_size, iterations):

#     val_loss_log = []
#     for i in range(iterations):
        
#         batch, label = epgen.get_episode(data, batch_size)

#         y_pred = np.round(model.predict([batch[0], batch[1]]))

#         val_loss = binary_crossentropy(label, y_pred, from_logits=True)
#         val_loss_log.append(val_loss)
    
#     val_loss_log = tf.convert_to_tensor(val_loss_log)
        
#     mean_val_loss = tf.math.reduce_mean(val_loss_log)
    
#     return mean_val_loss