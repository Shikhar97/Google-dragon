import os
import cv2
import time
import json
import pyautogui
import numpy as np

from pynput import keyboard


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
        self.training_data_file_path = 'labels.json'
        if os.path.exists(self.training_data_file_path):
            with open(self.training_data_file_path, "r+") as fp:
                self.labels = json.load(fp)
        else:
            self.labels = {}

    def grab_screen(self, region):
        im = pyautogui.screenshot(region=region)
        image = np.asarray(im)
        return image

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
        for i in list(range(4))[::-1]:
            print(i + 1)
            time.sleep(1)

        if not os.path.exists("data"):
            os.makedirs("data")
        file_names = os.listdir("data/")  # dir is your directory path
        file_no = len(file_names)
        while True:
            img_filename = "img" + str(file_no) + ".jpg"
            file_no += 1
            # original_screen = gb.mac_grab_screen(region=(0, 80, 675, 280))
            original_screen = self.grab_screen(region=(0, 400, 765, 700))
            with keyboard.Events() as events:
                event = events.get(0.5)
                if event is None:
                    output = self.key_to_one_hot(None)
                elif event.key == keyboard.KeyCode.from_char('q'):
                    with open(self.training_data_file_path, "w+") as fp:
                        json.dump(self.labels, fp)
                    cv2.destroyAllWindows()
                    return True
                else:
                    output = self.key_to_one_hot(str(event.key))
                print("Key pressed ", self.int_to_key[output])

            self.labels[img_filename] = output
            original_screen = cv2.cvtColor(original_screen, cv2.COLOR_BGR2GRAY)
            original_screen = cv2.resize(original_screen, (self.HEIGHT, self.WIDTH))

            # cv2.imshow("window", original_screen)
            cv2.imwrite(os.path.join("data", img_filename), original_screen)

            # training_data.append([original_screen, output])

            if self.count == 1:
                with open(self.training_data_file_path, "w+") as fp:
                    json.dump(self.labels, fp)
                cv2.destroyAllWindows()
                return True

            if len(self.labels) % 50 == 0:
                self.count += 1
                with open(self.training_data_file_path, "w+") as fp:
                    json.dump(self.labels, fp)
