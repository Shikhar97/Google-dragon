import cv2
import time

from grab_screen import grab_screen
from cnn_model import model

for i in list(range(4))[::-1]:
    print(i + 1)
    time.sleep(1)

HEIGHT = 224
WIDTH = 224
LEARNING_RATE = 1e-2
EPOCHS = 5
BATCH_SIZE = 30

dragon_model = model(HEIGHT, WIDTH, LEARNING_RATE, EPOCHS, BATCH_SIZE)

while (True):
    # original_screen =  grab_screen(region=(350,70,1000,280))
    original_screen = grab_screen(region=(0, 80, 675, 280))

    # last_time = time.time()
    original_screen = cv2.cvtColor(original_screen, cv2.COLOR_BGR2GRAY)
    original_screen = cv2.resize(original_screen, (HEIGHT, WIDTH))
    cv2.imshow("window", original_screen)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break