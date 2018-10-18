import pandas as pd
import cv2
import numpy as np
from collections import Counter

train_data = np.load('training_data.npy')

df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[1].apply(str)))
