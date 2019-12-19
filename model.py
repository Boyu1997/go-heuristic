import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization

def cnn_model():
    
    model = Sequential()

    model.add(Conv2D(32, (3, 3), activation ='relu', input_shape=(12,12,1)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation ='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size =(2, 2)))
    model.add(Flatten())

    model.add(Dense(200, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

    return model
