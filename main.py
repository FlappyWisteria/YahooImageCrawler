import os
from time import sleep

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_path = "./ImageScraping/chromedriver.exe"

input_box = input("What search ? --> ")

query = f"{input_box}"

options = Options()
options.add_argument("--incognito")
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')
driver = webdriver.Chrome(executable_path=chrome_path, options=options)

url = "https://search.yahoo.co.jp/image"
driver.get(url)

sleep(1)

search_box = driver.find_element_by_class_name('SearchBox__searchInput')
search_box.send_keys(query)
search_box.submit()

height = 0
while height < 10000:
    driver.execute_script(f"window.scrollTo(0,{height});")
    height += 500
    sleep(0.5)
    per = int(height) // 100
    print(f"Currently:{per}%")

sleep(1)

elements = driver.find_elements_by_class_name("sw-Thumbnail")

d_list = []

for i, e in enumerate(elements, start=1):
    name = f"{query}_{i}"
    image_url = e.find_element_by_tag_name("img").get_attribute("src")

    d = {
        "name": name,
        "image_url": image_url,
    }

    d_list.append(d)
    print(f"Output:{name}")
    sleep(0.05)

IMAGE_DIR_LOGS = "./ImageScraping/logs/"


if os.path.isdir(IMAGE_DIR_LOGS):
    print("Already")
else:
    os.makedirs(IMAGE_DIR_LOGS)

sleep(1)

df = pd.DataFrame(d_list)

df.to_csv(IMAGE_DIR_LOGS + "{}_image.csv".format(query))

driver.quit()

sleep(1)

csv_name = f"{query}_image.csv"
path = "./ImageScraping/logs/{}".format(csv_name)
df = pd.read_csv(path)

IMAGE_DIR = "./ImageScraping/images/{}/".format(query)


if os.path.isdir(IMAGE_DIR):
    print("Already")
else:
    os.makedirs(IMAGE_DIR)

for file_name, image_url in zip(df.name, df.image_url):
    image = requests.get(image_url)
    with open(IMAGE_DIR + file_name + ".png", "wb") as f:
        f.write(image.content)
    sleep(0.1)
    print(f"Saved:{file_name}")

print("Done")