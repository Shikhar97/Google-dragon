import numpy as np
import cv2
import time
import os

from getkeys import key_check
from grabscreen import grab_screen


def key_to_one_hot(keys):
    """
    Convert keys to a ...multi-hot... array

    [up arrow, down arrow] boolean values.
    """
    output = [0, 0]

    if 0x26 in keys:
        output[0] = 1
    elif 0x28 in keys:
        output[1] = 1
    return output


file_name = 'training_data.npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name))
else:
    print('File does not exist, starting fresh!')
    training_data = []

last_time = time.time()

for i in list(range(4))[::-1]:
    print(i + 1)
    time.sleep(1)

while (True):
    # original_screen =  grab_screen(region=(350,70,1000,280))
    original_screen = grab_screen(region=(0, 80, 675, 280))

    # last_time = time.time()
    original_screen = cv2.cvtColor(original_screen, cv2.COLOR_BGR2GRAY)
    original_screen = cv2.resize(original_screen, (224, 224))
    # cv2.imshow("window", original_screen)

    keys = key_check()
    output = key_to_one_hot(keys)
    training_data.append([original_screen, output])

    # print("output-> ",output)
    # print('loop took {} seconds'.format(time.time()-last_time))

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    if len(training_data) % 500 == 0:
            print(len(training_data))
            np.save(file_name,training_data)
