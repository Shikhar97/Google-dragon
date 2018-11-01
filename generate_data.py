import numpy as np
import cv2
import time
import os

from get_keys import key_check
from grab_screen import grab_screen

key_to_int = {"up": 0,
              "down": 1,
              "nothing": 2}

int_to_key = {
    0: "up",
    1: "down",
    2: "nothing"
}


def key_to_one_hot(keys):
    """
    Convert keys to a integer value.
    0x26 -> up(0)
    0x28 -> down(1)
    else -> nothing(2)
    """
    output = key_to_int["nothing"]

    if 0x26 in keys:
        output = key_to_int["up"]
    elif 0x28 in keys:
        output = key_to_int["down"]
    return output


training_data_file_path = 'training_data.npy'

if os.path.isfile(training_data_file_path):
    print('File exists, loading previous data!')
    training_data = list(np.load(training_data_file_path))
else:
    print('File does not exist, starting fresh!')
    training_data = []

last_time = time.time()

for i in list(range(4))[::-1]:
    print(i + 1)
    time.sleep(1)

HEIGHT = 224
WIDTH = 224

while (True):
    # original_screen =  grab_screen(region=(350,70,1000,280))
    original_screen = grab_screen(region=(0, 80, 675, 280))

    # last_time = time.time()
    original_screen = cv2.cvtColor(original_screen, cv2.COLOR_BGR2GRAY)
    original_screen = cv2.resize(original_screen, (HEIGHT, WIDTH))
    cv2.imshow("window", original_screen)

    keys = key_check()
    output = key_to_one_hot(keys)
    training_data.append([original_screen, output])
    print("Key pressed ", int_to_key[output])

    # print("output-> ",output)
    # print('loop took {} seconds'.format(time.time()-last_time))

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    if len(training_data) % 500 == 0:
        print(len(training_data))
        y = np.load(training_data_file_path) if os.path.isfile(training_data_file_path) else np.save(training_data_file_path, training_data)
        np.save(training_data_file_path, np.append(y,training_data))
        training_data = 0