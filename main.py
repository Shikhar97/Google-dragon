from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src import data_insight, generate_data as gd

gen_data = None
files_created = 0

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


# if game started generate the data
if element:
    gen_data = gd.DataGenerate()


if gen_data:
    files_created = gen_data.main()

# if data generated clean and compress it
if files_created:
    obj = data_insight.DataInsight()
    obj.main()
