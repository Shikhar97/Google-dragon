import pandas as pd
from collections import Counter
import numpy as np
from random import shuffle
import os


from src import generate_data as gd

class DataInsight:

    def __init__(self):

        self.gen_data = gd.DataGenerate()
        # self.train_data = np.load(self.gen_data.training_data_file_path+"1.npy")
        self.modified_training_data_file_path = "../data/training_data_v2.npy"
        # df = pd.DataFrame(self.train_data)
        # print(df.head())
        # print(Counter(df[1].apply(str)))

    def individualChoices(self, training_data_file_path):
        train_data = np.load(training_data_file_path)

        shuffle(train_data)

        up = []
        down = []
        nothing = []

        for data in train_data:
            img = data[0]
            move = data[1]
            if move == self.gen_data.key_to_int["up"]:
                up.append([img, move])
            elif move == self.gen_data.key_to_int["down"]:
                down.append([img, move])
            else:
                nothing.append([img, move])
        return up, down, nothing

    def main(self):
        final_data = []
        file_names = os.listdir("../data/")  # dir is your directory path
        number_files = len(file_names)
        file_names.sort()
        print(file_names)
        for i in range(number_files):
            print("file" + str(i + 1))

            up, down, nothing = self.individualChoices("../"+self.gen_data.training_data_file_path + str(i + 1) + ".npy")

            total_data_len = len(up) + len(down) + len(nothing)

            up_factor = len(up) / total_data_len
            down_factor = len(down) / total_data_len
            nothing_factor = len(nothing) / total_data_len

            up = up[:int(up_factor * len(up))]
            down = down[:int(down_factor * len(down))]
            nothing = nothing[:int(nothing_factor * len(nothing))]

            final_data += up + down + nothing
            shuffle(final_data)

        np.save(self.modified_training_data_file_path, final_data)

z=DataInsight()
z.main()
