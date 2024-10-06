from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from screeninfo import get_monitors

from time import sleep

import os

monitor = get_monitors()

# os.system('taskkill /im chrome.exe /f')

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument(f"--window-size={monitor[0].width},{monitor[0].height}")
chrome_options.add_argument("--allow-file-access-from-files")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

path_to_file = os.path.join(os.getcwd(), 'assets', 'index.html')

driver.get(f'file://{path_to_file}')

baner = driver.find_element(By.ID, "global_header")
bg = driver.find_element(By.CLASS_NAME, "no_header.profile_page.has_profile_background")

# bg.send_keys('/assets/bg.png')

driver.execute_script("""
   var baner = arguments[0];
   baner.parentNode.removeChild(baner);
""", baner)
driver.execute_script(f"""
   var bg = arguments[0];
   bg.style.backgroundImage = "url('bg.png')";
""", bg)
# driver.find_element(By.CLASS_NAME, "c-ripple").click()

sleep(1)

screenshot_path = "assets\\screenshot.png"
driver.save_screenshot(screenshot_path)

print(f"Скріншот збережено: {screenshot_path}")

# sleep(1111)

driver.quit()
