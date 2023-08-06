# add folder to system path
import os 
import sys
import random as rn
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

import tensorflow as tf
import logging

# to shut up tensorflow misc warnings
tf.get_logger().setLevel(logging.ERROR)
tf.autograph.set_verbosity(0)

import cv2
import numpy as np
import os
import glob
import time
import pydot
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm, trange

from tensorflow.keras import backend as K
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Model, Sequential, load_model
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, GlobalAveragePooling2D, Conv2DTranspose, BatchNormalization, Dropout, Flatten, Input, Reshape, Lambda, Concatenate, Add, Average, ReLU
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import mse, binary_crossentropy
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import plot_model

import scripts.ep_generator as epgen
# import scripts.gpu_setup
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)

# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#   try:
#     tf.config.experimental.set_virtual_device_configuration(gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=6000)])
#   except RuntimeError as e:
#     print(e)

# physical_devices = tf.config.list_physical_devices('GPU')
# try:
#     tf.config.experimental.(physical_devices[0], True)
#     tf.config.experimental.set_memory_growth(physical_devices[0], True)
# except:
#   # Invalid device or cannot modify virtual devices once initialized.
#     print("no physical devices")
#     pass



# print(gpus)

class Model_adm():
    """
    This is RelationNet class object. Use it to create a few-shot-compatible architecture.
    The original model architecture is preserved. You can set the input shape along with 
    the number of shots per label in the support and query sets.
    
    """
    class config():
        # set number of shots per episode
        anom  = 1 # anomaly brackets
        good  = 1 # template brackets
        query = 1 # test brackets
        input_shape = (256, 512, 3) # image size
        
        loss = binary_crossentropy
        optimizer = Adam
        eta = 1e-2
        batch_size = 4
        episodes = 100
        output="models/noName_v2.h5py"

    
    # MODEL GENERATION
    ##########################################################################################
    ##########################################################################################                
    def generate(self):
        seed = 656427
        tf.random.set_seed(seed)
        np.random.seed(seed)
        os.environ['PYTHONHASHSEED'] = str(seed)
        rn.seed(seed)
        
        def conv2D_block(layer, num, K_size=(3, 3), padding='same', BN=True):
            x = Conv2D(num, K_size, padding=padding)(layer)
            if BN:
                x = BatchNormalization()(x)
            x = ReLU()(x)

            return x


        # EMBEDDING MODULE f(x)
        ##########################################################################################
        input_layer = Input(shape=self.config.input_shape, name='input')

        x = conv2D_block(input_layer, 64)
        x = MaxPooling2D(strides=(2, 2))(x)
        x = conv2D_block(x, 64)
        x = MaxPooling2D(strides=(2, 2))(x)
        x = conv2D_block(x, 64)

        output_layer = conv2D_block(x, 64)

        feature_extractor = Model(input_layer, output_layer, name='FeatureExtractor')
        ##########################################################################################

        # RELATION MODULE g(x)
        ##########################################################################################
        tmp = feature_extractor.output_shape[1:]
        relation_input_shape = (tmp[0], tmp[1], tmp[2]*2)
        relation_input = Input(shape=relation_input_shape, name='relation_input')

        x = conv2D_block(relation_input, 64)
        x = MaxPooling2D(strides=(2, 2))(x)
        x = conv2D_block(x, 64)
        x = MaxPooling2D(strides=(2, 2))(x)
        x = GlobalAveragePooling2D()(x)
        x = Dense(8, activation='relu')(x)
        x = BatchNormalization()(x) # remove Dropout if adding BN
#         x = Dropout(0.25)(x) # remove BN if adding Dropout

        metric_output = Dense(1, activation='sigmoid')(x)

        metric_module = Model(relation_input, metric_output, name='metric_module')    
        ##########################################################################################

        
        # RELATION NETWORK
        ##########################################################################################
        # put all the inputs into a single array in order <anomalies, good, query>
        inputs = []
        for i in range(self.config.anom):
            inputs.append(Input(self.config.input_shape, name='input_anom_' + str(i)))
        for i in range(self.config.good):
            inputs.append(Input(self.config.input_shape, name='input_good_' + str(i)))
        for i in range(self.config.query):
            inputs.append(Input(self.config.input_shape, name='input_query_' + str(i)))

        
        # extract the embeddings for every input
        embeddings = []
        for layer in inputs:
            embeddings.append(feature_extractor(layer))

        # make the fusion layers (few-shot) in the support set (anomalies and good)
        fusion_anom  = Add(name='Fusion_Anom')(embeddings[0: self.config.anom])
        fusion_good  = Add(name='Fusion_Good')(embeddings[self.config.anom: self.config.good + self.config.anom])
        
        # concatenate the two fusion layers with each query embedding
        concat_anom_query = []
        concat_good_query = []
        for i, query in enumerate(embeddings[-self.config.query:]):
            concat_anom_query.append(Concatenate(name='Concat_Anom_' + str(i))([fusion_anom, query]))
            concat_good_query.append(Concatenate(name='Concat_Good_' + str(i))([fusion_good, query]))
        
        # pass every relational feature through the relation module g(x)
        relations_anom = []
        relations_good = []
        for relation_anom_query, relation_good_query in zip(concat_anom_query, concat_good_query):
            relations_anom.append(metric_module(relation_anom_query))
            relations_good.append(metric_module(relation_good_query))
        
        # a lambda layer for put together the two relation scores (<anom vs query> and <good vs query>)
        def concat_relations(items):
            relations_anom = tf.concat(items[0], axis=-1)
            relations_good = tf.concat(items[1], axis=-1)

            return tf.stack([relations_anom, relations_good], axis=-1)
        relation_output = Lambda(concat_relations)([relations_anom, relations_good])

        
        return Model(inputs, outputs=relation_output, name='RelationNet')                
    ##########################################################################################
    ##########################################################################################
    
    # TRAIN    
    def fit(self, train_data, test_data, model):
        seed = 656427
        tf.random.set_seed(seed)
        np.random.seed(seed)
        os.environ['PYTHONHASHSEED'] = str(seed)
        rn.seed(seed)
        
        eta=self.config.eta
        batch_size=self.config.batch_size
        episodes=self.config.episodes
        output=self.config.output
            
            
        # custom loss
        def loss_fn(y, y_pred):
            return tf.math.reduce_mean(binary_crossentropy(y, y_pred, from_logits=True))
        
        def compile(self):        
            model.compile(optimizer=self.config.optimizer(self.config.eta), loss=loss_fn)
            print("Model compiled.")
        
        compile(self)
        
        # validation function
        def validate(model, data, batch_size, anom_shots, good_shots, query_shots):
            iterations = (data[0].shape[0] + data[1].shape[0]) * 2 // (batch_size*2)
            
            val_loss_log = []
            for i in range(iterations):

                X, y = epgen.gen_episode(data, anom_shots, good_shots, query_shots, batch_size)

                logits = model.predict(X)

                val_loss = loss_fn(y, logits)
                val_loss_log.append(val_loss)

            val_loss_log = tf.convert_to_tensor(val_loss_log)        
            mean_val_loss = K.eval(tf.math.reduce_mean(val_loss_log))

            return mean_val_loss        
        
        
        # misc
        episodes += 1
        val_loss_past = np.inf
        

        log_ep_labels  = []
        log_loss = []
        log_val_loss = []
        
        optimizer = self.config.optimizer

        print("\nTraining...\n")
        for i in trange(episodes):                        
            
            X, y = epgen.gen_episode(train_data, self.config.anom, self.config.good, self.config.query, batch_size)

            with tf.GradientTape() as tape:

                logits = model(X, training=True)
                loss = loss_fn(y, logits)

#                 log_ep_labels.append(K.eval(label)[0][0])
                log_loss.append(K.eval(tf.math.reduce_mean(loss)))

            
            grads = tape.gradient(loss, model.trainable_weights)            
            optimizer = Adam(self.config.eta)
            optimizer.apply_gradients(zip(grads, model.trainable_weights))
            

            if (i+1) % 100 == 0:

                print("Validating...")

                val_loss = validate(model, test_data, batch_size*2, self.config.anom, self.config.good, self.config.query)
                log_val_loss.append(val_loss)            

                if val_loss < val_loss_past:
                    print("\nMODEL IMPROVED, saving...\n best loss:", val_loss)
                    model.save(output)
                    print("")
                    val_loss_past = val_loss
                else:
                    print("\nVal_loss not improved:", val_loss)
                    print("val_loss_best:", val_loss_past)

#                 result = list(zip(log_loss, log_ep_labels))
#                 step = int(i * 0.00033 + 1)
#                 plot_loss(result[::step], val_loss_log[::step], 50)

#             if (i+1) >= 10
#                 val_loss_log.append(val_loss)

            if (i+1) % 2000 == 0:
                self.config.eta *= 0.75
                compile(self)
                print("\nUpdating eta to...", self.config.eta)


            # Log 
            if i % 10 == 0:
                print(
                    "epoch:", str(i), "/", episodes, " | loss:", loss.numpy())
            

        return log_loss, log_val_loss

        
    # EVALUATE ACCURACY
    def evaluate(self, data, model, iterations):
        seed = 656427
        tf.random.set_seed(seed)
        np.random.seed(seed)
        os.environ['PYTHONHASHSEED'] = str(seed)
        rn.seed(seed)
        
        print("Evaluating model...\n")
        total = iterations * self.config.batch_size * self.config.query
        log = []
        for i in trange(iterations):
            inner_log = []
            for i in range(100):
                X, y = epgen.gen_episode(data,
                                         self.config.anom,
                                         self.config.good,
                                         self.config.query,
                                         self.config.batch_size)

                pred = model(X).numpy()
                test = np.argmax(y, axis=2) == np.argmax(pred, axis=2)    
                test = (test * 1)

                inner_log.append(test)
            log.append(np.array(inner_log).mean())

        log = np.array(log)
        mean_acc = log.mean()
        std_acc = log.std()
        print("Accuracy:", round(mean_acc*100, 2), "+-", round(std_acc*1.96*100, 2), "%")            

        return mean_acc, std_acc