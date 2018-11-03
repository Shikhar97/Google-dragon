# import cv2
# import time
#
# from src.grab_screen import grab_screen
# from cnn_model import model
#
# for i in list(range(4))[::-1]:
#     print(i + 1)
#     time.sleep(1)
#
# HEIGHT = 224
# WIDTH = 224
# LEARNING_RATE = 1e-2
# EPOCHS = 5
# BATCH_SIZE = 30
#
# dragon_model = model(HEIGHT, WIDTH, LEARNING_RATE, EPOCHS, BATCH_SIZE)
#
# while (True):
#     # original_screen =  grab_screen(region=(350,70,1000,280))
#     original_screen = grab_screen(region=(0, 80, 675, 280))
#
#     # last_time = time.time()
#     original_screen = cv2.cvtColor(original_screen, cv2.COLOR_BGR2GRAY)
#     original_screen = cv2.resize(original_screen, (HEIGHT, WIDTH))
#     cv2.imshow("window", original_screen)
#
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()
#         break


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from src import data_insight, generate_data as gd

chrome_path = "chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
# opening the browser
browser = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)

# setting the window position
browser.set_window_position(-7, 0)
browser.set_window_size(782, 831)

# opening in offline mode
browser.set_network_conditions(offline=True, latency=5, throughput=500 * 1024)
browser.get('http://www.google.com')

# starting the game
element = browser.find_element_by_id("t")

gen_data = None
files_created = 0

# if game started generate the data
if element:
    element.send_keys(Keys.ARROW_UP)
    print("Game Started")
    gen_data = gd.DataGenerate()


if gen_data:
    files_created = gen_data.main()

# if data generated clean and compress it
if files_created:
    obj = data_insight.DataInsight()
    obj.main()

# print(browser.get_window_size())
# driver.quit()
