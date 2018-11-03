import numpy as np
import cv2
import time
import os

from src import grab_screen as gb, get_keys as gk


class DataGenerate():
    def __init__(self):
        self.key_to_int = {
            "up": 0,
            "down": 1,
            "nothing": 2
        }
        self.int_to_key = {
            0: "up",
            1: "down",
            2: "nothing"
        }
        self.HEIGHT = 224
        self.WIDTH = 224
        self.count = 0
        self.training_data_file_path = 'data/training_data'

    def key_to_one_hot(self, keys):
        """
        Convert keys to a integer value.
        0x26 -> up(0)
        0x28 -> down(1)
        else -> nothing(2)
        """
        output = self.key_to_int["nothing"]

        if 0x26 in keys:
            output = self.key_to_int["up"]
        elif 0x28 in keys:
            output = self.key_to_int["down"]
        return output

    def main(self):
        if os.path.isfile(self.training_data_file_path):
            print('File exists, loading previous data!')
            training_data = list(np.load(self.training_data_file_path))
        else:
            print('File does not exist, starting fresh!')
            training_data = []
            # np.save(self.training_data_file_path, training_data)

        last_time = time.time()

        for i in list(range(4))[::-1]:
            print(i + 1)
            time.sleep(1)
        file_names = os.listdir("data/")  # dir is your directory path
        number_files = len(file_names)
        self.count = number_files
        while (True):
            original_screen = gb.grab_screen(region=(0, 80, 675, 280))
            # last_time = time.time()
            original_screen = cv2.cvtColor(original_screen, cv2.COLOR_BGR2GRAY)
            original_screen = cv2.resize(original_screen, (self.HEIGHT, self.WIDTH))
            cv2.imshow("window", original_screen)
            keys = gk.key_check()
            output = self.key_to_one_hot(keys)
            training_data.append([original_screen, output])
            print("Key pressed ", self.int_to_key[output])

            # print("output-> ",output)
            # print('loop took {} seconds'.format(time.time()-last_time))

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            if len(training_data) % 5000 == 0:
                self.count += 1
                print(len(training_data))
                # y = np.load(self.training_data_file_path)
                # if os.path.isfile(training_data_file_path + '.npy'):
                print("file name to be written -> ", self.training_data_file_path + str(self.count) + ".npy")
                np.save(self.training_data_file_path + str(self.count) + ".npy", training_data)
                training_data = []
                if self.count == 10:
                    cv2.destroyAllWindows()
                    break
# z=DataGenerate()
# z.main()