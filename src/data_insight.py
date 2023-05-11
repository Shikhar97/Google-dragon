import json

import numpy as np
from random import shuffle
import os

from src import generate_data as gd


class DataInsight:

    def __init__(self):

        self.gen_data = gd.DataGenerate()
        self.modified_training_data_file_path = "labels_v2.json"

    def individualChoices(self, training_data_file_path):
        with open(training_data_file_path, "r+") as fp:
            train_data = json.load(fp)

        shuffle(train_data)

        up = []
        down = []
        nothing = []

        for img, move in train_data:
            if move == self.gen_data.key_to_int["up"]:
                up.append({img: move})
            elif move == self.gen_data.key_to_int["down"]:
                down.append({img: move})
            else:
                nothing.append({img: move})
        return up, down, nothing

    def main(self):
        final_data = []
        # # dir is your directory path
        # file_names = os.listdir("data/")
        # number_files = len(file_names)
        # file_names.sort()
        # print(file_names)
        # for i in range(number_files):
        up, down, nothing = self.individualChoices(self.gen_data.training_data_file_path)

        total_data_len = len(up) + len(down) + len(nothing)

        up_factor = len(up) / total_data_len
        down_factor = len(down) / total_data_len
        nothing_factor = len(nothing) / total_data_len

        up = up[:int(up_factor * len(up))]
        down = down[:int(down_factor * len(down))]
        nothing = nothing[:int(nothing_factor * len(nothing))]

        final_data += up + down + nothing
        print(final_data)
        shuffle(final_data)

        # np.save(self.modified_training_data_file_path, final_data)

# to run this file independently
# z=DataInsight()
# z.main()
