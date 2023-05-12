from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

from src import data_insight, generate_data as gd

files_created = False
game_url = "chrome://dino/"

options = webdriver.ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
options.page_load_strategy = "normal"
options.add_experimental_option("detach", True)

# opening the browser
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

wait = WebDriverWait(driver, 300)

# setting the window position
driver.set_window_position(-7, 0)
driver.set_window_size(782, 831)

# opening in offline mode
# driver.set_network_conditions(offline=True, latency=5, throughput=500 * 1024)
try:
    driver.get(game_url)
except WebDriverException:
    pass

# starting the game
wait.until(EC.visibility_of_element_located((By.ID, "t"))).send_keys(Keys.SPACE)

# if game started generate the data
gen_data = gd.DataGenerate()

if gen_data:
    files_created = gen_data.main()
    driver.close()
    driver.quit()

# if data generated clean and compress it
if files_created:
    obj = data_insight.DataInsight()
    obj.main()
