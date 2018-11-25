import numpy as np
import cv2
import time
import os

from src import grab_screen as gb, get_keys as gk


class DataGenerate:
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
        training_data = []
        for i in list(range(4))[::-1]:
            print(i + 1)
            time.sleep(1)

        file_names = os.listdir("data/")  # dir is your directory path
        number_files = len(file_names)
        self.count = number_files
        while self.count < 50 and True:

            # original_screen = gb.grab_screen(region=(0, 80, 675, 280))
            original_screen = gb.grab_screen(region=(0, 100, 900, 340))

            keys = gk.key_check()
            output = self.key_to_one_hot(keys)

            original_screen = cv2.cvtColor(original_screen, cv2.COLOR_BGR2GRAY)

            original_screen = cv2.resize(original_screen, (self.HEIGHT, self.WIDTH))
            cv2.imshow("window", original_screen)

            training_data.append([original_screen, output])
            print("Key pressed ", self.int_to_key[output])

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            if len(training_data) % 2500 == 0:
                self.count += 1
                print("file name to be written -> ", self.training_data_file_path + str(self.count) + ".npy")
                np.save(self.training_data_file_path + str(self.count) + ".npy", training_data)
                training_data = []
                if self.count == 50:
                    cv2.destroyAllWindows()
                    return True
        return False

# to run this file indenpendently
# z=DataGenerate()
# z.main()
