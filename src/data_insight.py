import json
from src import generate_data as gd


class DataInsight:

    def __init__(self):

        self.gen_data = gd.DataGenerate()
        self.modified_training_data_file_path = "labels_v2.json"

    def individual_choices(self, training_data_file_path):
        with open(training_data_file_path, "r+") as fp:
            train_data = json.load(fp)

        up = []
        down = []
        nothing = []
        for img, move in train_data.items():
            if move == self.gen_data.key_to_int["up"]:
                up.append({img: move})
            elif move == self.gen_data.key_to_int["down"]:
                down.append({img: move})
            else:
                nothing.append({img: move})
        return up, down, nothing

    def main(self):
        final_data = []
        labels = {}
        up, down, nothing = self.individual_choices(self.gen_data.training_data_file_path)

        total_data_len = len(up) + len(down) + len(nothing)

        up_factor = len(up) / total_data_len
        down_factor = len(down) / total_data_len
        nothing_factor = len(nothing) / total_data_len

        up = up[:int(up_factor * len(up))]
        down = down[:int(down_factor * len(down))]
        nothing = nothing[:int(nothing_factor * len(nothing))]

        final_data += up + down + nothing
        for img in final_data:
            labels.update(img)
        with open(self.modified_training_data_file_path, "w+") as fp:
            json.dump(labels, fp)
