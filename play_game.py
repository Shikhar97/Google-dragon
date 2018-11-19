import numpy as np
import cv2
import time
import os

from keras.engine.saving import model_from_json
import keras.utils
import keras.losses

from src import grab_screen as gb, get_keys as gk
from src.direct_keys import PressKey, ReleaseKey, up_arrow, down_arrow
from src.generate_data import DataGenerate as dg
from src.get_keys import key_check


def up():
    PressKey(up_arrow)
    ReleaseKey(down_arrow)

def down():
    PressKey(down_arrow)
    ReleaseKey(up_arrow)

def nothing():
    ReleaseKey(up_arrow)
    ReleaseKey(down_arrow)

def cnn_model():
    json_file = open('model/cnn_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")
    loaded_model.compile(loss=keras.losses.categorical_crossentropy,
                   optimizer=keras.optimizers.Adam(), metrics=['accuracy'])
    return loaded_model

def main():
    last_time = time.time()

    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False

    while (True):
        if not paused:
            original_screen = gb.grab_screen(region=(0, 80, 675, 280))
            # last_time = time.time()
            original_screen = cv2.cvtColor(original_screen, cv2.COLOR_BGR2GRAY)
            original_screen = cv2.resize(original_screen, (dg.HEIGHT, dg.WIDTH))

            original_screen = np.array(original_screen)
            original_screen.reshape(-1, dg.HEIGHT, dg.WIDTH, 1)
            original_screen = original_screen.astype('float32')
            original_screen = original_screen / 255

            move = (cnn_model().predict(original_screen)).argmax()
            if(dg.int_to_key(move) == 'up'):
                up()
            elif(dg.int_to_key(move) == 'down'):
                down()
            else:
                nothing()

        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(up_arrow)
                ReleaseKey(down_arrow)
                time.sleep(1)