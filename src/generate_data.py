import numpy as np
import json
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
        with open("labels.json", "r+") as fp:
            self.labels = json.load(fp)

    def key_to_one_hot(self, keys):
        """
        Convert keys to a integer value.
        "Key.up" -> up(0)
        "Key.down" -> down(1)
        else -> nothing(2)
        """
        output = self.key_to_int["nothing"]

        if "Key.up" == keys:
            output = self.key_to_int["up"]
        elif "Key.down" == keys:
            output = self.key_to_int["down"]
        return output

    def main(self):
        training_data = []
        for i in list(range(4))[::-1]:
            print(i + 1)
            time.sleep(1)

        if not os.path.exists(os.path.dirname(self.training_data_file_path)):
            os.makedirs(os.path.dirname(self.training_data_file_path))
        file_names = os.listdir("data/")  # dir is your directory path
        file_no = len(file_names)
        self.count = file_no
        while self.count < 50 and True:
            img_filename = "img" + str(file_no)
            file_no += 1
            # original_screen = gb.mac_grab_screen(region=(0, 80, 675, 280))
            original_screen = gb.mac_grab_screen(region=(0, 370, 765, 670))

            keys = gk.get_key()
            output = self.key_to_one_hot(keys)

            original_screen = cv2.cvtColor(original_screen, cv2.COLOR_BGR2GRAY)

            original_screen = cv2.resize(original_screen, (self.HEIGHT, self.WIDTH))

            # cv2.imshow("window", original_screen)
            cv2.imwrite(img_filename, original_screen)
            self.labels[img_filename] = output

            # training_data.append([original_screen, output])
            print("Key pressed ", self.int_to_key[output])

            if gk.get_key() == 'q' or self.count == 50:
                with open("labels.json") as fp:
                    json.dump(self.labels, fp)
                cv2.destroyAllWindows()
                return True

            if len(training_data) % 25 == 0:
                self.count += 1
            #     print("file name to be written -> ", self.training_data_file_path + str(self.count) + ".npy")
            #     np.save(self.training_data_file_path + str(self.count) + ".npy", training_data)
            #     training_data = []
            #     if
            #         return True
        return False

# to run this file independently
# z=DataGenerate()
# z.main()
