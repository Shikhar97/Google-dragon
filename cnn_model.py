import numpy as np
import keras.utils
import keras.losses
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from random import shuffle

from src import data_insight
from src.get_keys import no_of_classes

HEIGHT = 224
WIDTH = 224
epochs = 5
batch_size = 30

split_factor = 0.8

obj = data_insight.DataInsight()


# prepare training and testing samples
def splitdata(path):
    up, down, nothing = obj.individualChoices(path)
    shuffle(up)
    shuffle(down)
    shuffle(nothing)

    train_data = up[:int(split_factor * len(up))] + down[:int(split_factor * len(down))] \
                 + nothing[:int(split_factor * len(nothing))]

    test_data = up[int(split_factor * len(up)):] + down[int(split_factor * len(down)):] \
                + nothing[int(split_factor * len(nothing)):]

    shuffle(train_data)
    shuffle(test_data)
    return train_data, test_data


# spliting training data to training and validation set
def train_split_validation(train_x, train_one_hot, split_factor):
    return_train_x = []
    return_train_y = []
    return_valid_x = []
    return_valid_y = []

    up = []
    down = []
    nothing = []
    print(len(train_x))
    for encoding, image in zip(train_one_hot, train_x):
        if (encoding.argmax() == 0):
            up.append([image, encoding])
        elif (encoding.argmax() == 1):
            down.append([image, encoding])
        else:
            nothing.append([image, encoding])

    shuffle(up)
    shuffle(down)
    shuffle(nothing)

    train_data = up[:int(split_factor * len(up))] + down[:int(split_factor * len(down))] \
                 + nothing[:int(split_factor * len(nothing))]

    validation_data = up[int(split_factor * len(up)):] + down[int(split_factor * len(down)):] \
                      + nothing[int(split_factor * len(nothing)):]

    for train in train_data:
        return_train_x.append(train[0])
        return_train_y.append(train[1])
    for valid in validation_data:
        return_valid_x.append(valid[0])
        return_valid_y.append(valid[1])

    return np.array(return_train_x), np.array(return_valid_x), np.array(return_train_y), np.array(return_valid_y)


training_data, testing_data = splitdata(obj.modified_training_data_file_path)


train_x = np.array([i[0] for i in training_data])
train_y = np.array([i[1] for i in training_data])

test_x = np.array([i[0] for i in testing_data])
test_y = np.array([i[1] for i in testing_data])

# prepare data to feed into the CNN
train_x = train_x.reshape(-1, HEIGHT, WIDTH, 1)
test_x = test_x.reshape(-1, HEIGHT, WIDTH, 1)

# Convert into float and normalize
train_x = train_x.astype('float32')
test_x = test_x.astype('float32')
train_x = train_x / 255
test_x = test_x / 255


# convert labels into one_hot_vector
train_y_one_hot = keras.utils.to_categorical(train_y)
test_y_one_hot = keras.utils.to_categorical(test_y)


# split data into training and validation
train_x, valid_x, train_y, valid_y = train_split_validation(train_x, train_y_one_hot, split_factor)

# ready to train
MODEL_FILE_NAME = "cnn_model.json"
WEIGHT_FILE_NAME = "cnn_model.h5"


def model(height, width, epochs, batch_size):
    dragon = Sequential()
    dragon.add(Conv2D(32, kernel_size=3, input_shape=(height, width, 3), padding="valid"))
    dragon.add(LeakyReLU(alpha=0.1))
    dragon.add(MaxPooling2D(2, 2))

    dragon.add(Conv2D(16, kernel_size=3, padding="valid"))
    dragon.add(LeakyReLU(alpha=0.1))
    dragon.add(MaxPooling2D(2, 2))

    dragon.add(Conv2D(8, kernel_size=3, padding="valid"))
    dragon.add(LeakyReLU(alpha=0.1))
    dragon.add(MaxPooling2D(2, 2))

    dragon.add(Flatten())

    dragon.add(Dense(128))
    dragon.add(LeakyReLU(alpha=0.1))
    dragon.add(Dense(no_of_classes, activation="softmax"))

    dragon.summary()

    dragon.compile(loss=keras.losses.categorical_crossentropy,
                   optimizer=keras.optimizers.Adam(), metrics=['accuracy'])

    history = dragon.fit(train_x, train_y, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(valid_x, valid_y))
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    
    # Test out the Model
    test_eval = dragon.evaluate(test_x, test_y_one_hot, verbose=0)
    print('Test loss:', test_eval[0])
    print('Test accuracy:', test_eval[1])

    dragon_json = dragon.to_json()
    with open("model/dragon_cnn.json", "w") as json_file:
        json_file.write(dragon_json)

    # serialize weights to HDF5
    dragon.save_weights("model/dragon_cnn.h5")
    print("Saved model to disk")


model(WIDTH, HEIGHT, epochs, batch_size)
