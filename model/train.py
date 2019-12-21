import json
import numpy as np
import pandas as pd

from keras.backend import reshape
from keras.utils.np_utils import to_categorical
from keras.callbacks import ModelCheckpoint

from model import cnn_model


def train(heuristic_model_iteration=None):
    if heuristic_model_iteration != None:
        data_path = 'data/iteration-{:02d}-data.json'.format(heuristic_model_iteration)
        model_path = 'save/iteration-{:02d}-weights.hdf5'.format(heuristic_model_iteration)
    else:
        data_path = 'data.json'
        model_path = 'weights.hdf5'

    with open(data_path) as f:
        df = pd.read_json(f)

    X = np.array(df['data'].values.tolist()).reshape(-1,12,12,1)
    y = to_categorical(df['label'], num_classes=2)
    print ("data count by class:", np.sum(y, axis=0))

    train_validate_split = 0.8
    s = int(len(df) * train_validate_split)
    X_train, X_test, y_train, y_test = X[:s], X[s:], y[:s], y[s:]

    class_count = np.sum(y_train, axis=0)
    class_weight = {0: class_count[0], 1: class_count[1]}

    model = cnn_model()
    if heuristic_model_iteration >= 1:   # new model trained base on last model
        model.load_weights('save/iteration-{:02d}-weights.hdf5'.format(heuristic_model_iteration-1))

    mc = ModelCheckpoint(model_path,
                         save_best_only=True,
                         monitor='val_loss',
                         mode='min',
                         save_weights_only=True)

    history = model.fit(X_train,
                        y_train,
                        class_weight=class_weight,
                        validation_data=(X_test, y_test),
                        epochs=5,
                        batch_size=512,
                        callbacks=[mc])
