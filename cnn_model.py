import numpy as np
import keras.utils
import keras.losses
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from random import shuffle
from sklearn.model_selection import train_test_split

from src import data_insight
from src.get_keys import no_of_classes


HEIGHT = 224
WIDTH  = 224


split_factor = 0.8

obj = data_insight.DataInsight()


# prepare training and testing samples
def splitData(path):

    up, down, nothing = obj.individualChoices(path)
    shuffle(up)
    shuffle(down)
    shuffle(nothing)

    train_data = up[:int(split_factor * len(up))] + down[:int(split_factor * len(down))] \
                 + nothing[:int(split_factor * len(nothing))]

    test_data = up[-int(split_factor * len(up)):] + down[-int(split_factor * len(down)):] \
                + nothing[-int(split_factor * len(nothing)):]

    shuffle(train_data)
    shuffle(test_data)
    return train_data, test_data


training_data, testing_data = splitData(obj.modified_training_data_file_path)

train_x = np.array([i[0] for i in training_data])
train_y = np.array([i[1] for i in training_data])
# train_y = list(set(tuple(x) for x in train_y))

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

print(train_x.shape)
print(train_y_one_hot.shape)


# split data into training and validation
train_x, valid_x, train_y, valid_y = train_test_split(train_x, train_y_one_hot, test_size=0.2)

# ready to train
MODEL_FILE_NAME = "cnn_model.json"
WEIGHT_FILE_NAME = "cnn_model.h5"


def model(height, width, epochs, batch_size):
    dragon = Sequential()
    dragon.add(Conv2D(8, kernel_size=3, input_shape=(height, width, 1), padding="valid"))
    dragon.add(LeakyReLU(alpha=0.1))
    dragon.add(MaxPooling2D(2, 2))

    dragon.add(Conv2D(16, kernel_size=3, padding="valid"))
    dragon.add(LeakyReLU(alpha=0.1))
    dragon.add(MaxPooling2D(2, 2))

    dragon.add(Conv2D(32, kernel_size=3, padding="valid"))
    dragon.add(LeakyReLU(alpha=0.1))
    dragon.add(MaxPooling2D(2, 2))

    dragon.add(Flatten())

    dragon.add(Dense(128))
    dragon.add(LeakyReLU(alpha=0.1))
    dragon.add(Dense(no_of_classes, activation="softmax"))

    dragon.summary()

    dragon.compile(loss=keras.losses.categorical_crossentropy,
                   optimizer=keras.optimizers.Adam(), metrics=['accuracy'])

    dragon.fit(train_x, train_y, batch_size=batch_size,
                              epochs=epochs, verbose=1,
                              validation_data=(valid_x, valid_y))
    # Test out the Model

    test_eval = dragon.evaluate(test_x, test_y_one_hot, verbose=0)
    print('Test loss:', test_eval[0])
    print('Test accuracy:', test_eval[1])


model(224, 224, 10, 30)