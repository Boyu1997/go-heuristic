import json
import numpy as np
import pandas as pd

from keras.backend import reshape
from keras.utils.np_utils import to_categorical
from keras.callbacks import ModelCheckpoint

from model import cnn_model


with open('data.json') as f:
    df = pd.read_json(f)

X = np.array(df['data'].values.tolist()).reshape(-1,12,12,1)
y = to_categorical(df['label'])

train_validate_split = 0.8
s = int(len(df) * train_validate_split)
X_train, X_test, y_train, y_test = X[:s], X[s:], y[:s], y[s:]

model = cnn_model()
mc = ModelCheckpoint('save/weights{epoch:02d}.h5',
                     save_weights_only=True, period=1)
history = model.fit(X_train,
                    y_train,
                    validation_data=(X_test, y_test),
                    epochs=5,
                    batch_size=512,
                    callbacks=[mc])
