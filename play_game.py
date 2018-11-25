import numpy as np
import cv2
import time

import keras.utils
import keras.losses
from keras.models import model_from_json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from src import grab_screen as gb
from src.direct_keys import PressKey, ReleaseKey, up_arrow, down_arrow
from src.generate_data import DataGenerate
from src.get_keys import key_check

dg = DataGenerate()


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
    json_file = open('model/dragon_cnn.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights("model/dragon_cnn.h5")
    print("Loaded model from disk")
    loaded_model.compile(loss=keras.losses.categorical_crossentropy,
                         optimizer=keras.optimizers.Adam(), metrics=['accuracy'])
    return loaded_model


def main():

    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False
    loaded_model = cnn_model()
    element = browser.find_element_by_id("t")
    while True:
        if not paused:
            # original_screen = gb.grab_screen(region=(0, 80, 675, 280))
            original_screen = gb.grab_screen(region=(0, 100, 900, 340))

            original_screen = cv2.cvtColor(original_screen, cv2.COLOR_BGR2GRAY)
            original_screen = cv2.resize(original_screen, (dg.HEIGHT, dg.WIDTH))

            original_screen = np.array(original_screen)
            original_screen = original_screen.reshape(-1, dg.HEIGHT, dg.WIDTH, 1)

            original_screen = original_screen.astype('float32')
            original_screen = original_screen / 255

            move = loaded_model.predict(original_screen)

            # print(move)
            t_move = move.argmax()

            if dg.int_to_key[t_move] == 'up':
                element.send_keys(Keys.ARROW_UP)

            elif dg.int_to_key[t_move] == 'down':
                element.send_keys(Keys.ARROW_DOWN)
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


chrome_path = "chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
# opening the browser
browser = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)

# setting the window position
browser.set_window_position(-7, 0)
browser.set_window_size(782, 831)

# opening in offline mode
browser.set_network_conditions(offline=True, latency=5, throughput=500 * 1024)
browser.get('http://www.google.com')

# starting the game
element = browser.find_element_by_id("t")

gen_data = None
files_created = 0

# if game started generate the data
if element:
    main()
    time.sleep(5)
    # element.send_keys(Keys.ARROW_UP)
    print("Game Started")
