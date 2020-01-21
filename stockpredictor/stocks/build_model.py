# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 10:34:32 2020

@author: Josh
"""
from tensorflow import keras
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from services import get_stock
from django.conf import settings

#run one time to create generic model

spy, _ = get_stock()

def generate_model(X, y, model_output = None):
    
    model = keras.models.Sequential([
    keras.layers.Dense(32, input_shape = (X.shape[1], ), activation = 'relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(32, activation = 'relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(16, activation = 'relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(1)])

    model.compile(loss = 'mean_squared_error', optimizer = 'adam')
    model_history = model.fit(X, y, validation_split = 0.20, epochs = 50, verbose = 1)
    
    keras.models.save_model(model, model_output)
    
    return model


features = ['Close', 'Open', 'High', 'Low', 'Volume']

for feature in features:
    
    X = spy.drop(feature, axis = 1)
    y = spy[feature]
    
    X['Date'] = np.arange(0, len(X))
    
    X = X.to_numpy()
    y = y.to_numpy()
    
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    model = generate_model(X, y, model_output = '{0}/stocks/models/{1}_model.h5'.format(settings.MODEL_DIR, feature))