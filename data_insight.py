import pandas as pd
import numpy as np
from collections import Counter
from random import shuffle

from generate_data import key_to_int, training_data_file_path

train_data = np.load(training_data_file_path)

df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[1].apply(str)))


def individualChoices(trainig_data_file_path):
    train_data = np.load(trainig_data_file_path)
    shuffle(train_data)

    up = []
    down = []
    nothing = []

    for data in train_data:
        img = data[0]
        move = data[1]
        if move == key_to_int["up"]:
            up.append([img, move])
        elif move == key_to_int["down"]:
            down.append([img, move])
        else:
            nothing.append([img, move])
    return (up, down, nothing)


up, down, nothing = individualChoices(training_data_file_path)

lowestDataSize = min(len(up), len(down), len(nothing))

up = up[:lowestDataSize]
down = down[:lowestDataSize]
nothing = nothing[:lowestDataSize]

final_data = up + down + nothing
shuffle(final_data)

modified_training_data_file_path = "training_data_v2.npy"
np.save(modified_training_data_file_path, final_data)
