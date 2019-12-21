import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization, LeakyReLU

def cnn_model():

    model = Sequential()

    model.add(Conv2D(16, (3, 3), padding='same', input_shape=(12,12,1)))
    model.add(LeakyReLU(alpha=0.3))
    model.add(BatchNormalization())
    model.add(Conv2D(32, (3, 3), padding='same'))
    model.add(LeakyReLU(alpha=0.3))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3), padding='same'))
    model.add(LeakyReLU(alpha=0.3))
    model.add(BatchNormalization())
    model.add(Conv2D(48, (3, 3), padding='same'))
    model.add(LeakyReLU(alpha=0.3))
    model.add(BatchNormalization())
    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(LeakyReLU(alpha=0.3))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size =(2, 2)))
    model.add(Flatten())

    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(2, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

    return model


if __name__ == "__main__":
    model = cnn_model()
    model.summary()
