from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

driver = webdriver.Chrome()

urls = [
    "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=2&proptype=Multistorey-Apartment&cityName=Pune"
]

query = "pune_2BHK_baner"
file_counter = 0

scroll_pause_time = 5
scroll_range = 10000
scrolls_per_url = 1

for url in urls:
    driver.get(url)
    input("apply filter and press enter:")
    output_dir = f"./Magicbricks_final_final/{query}_url_{urls.index(url)}"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for _ in range(scrolls_per_url):
        driver.execute_script(f"window.scrollBy(0, {scroll_range});")

        time.sleep(scroll_pause_time)

    elems = driver.find_elements(By.CSS_SELECTOR, ".mb-srp__card")
    print(f"{len(elems)} elements found ")

    for elem in elems:
        d = elem.get_attribute("outerHTML")

        with open(
            f"{output_dir}/{query}_{file_counter}.html", "w", encoding="utf-8"
        ) as f:
            f.write(d)

        file_counter += 1

    print(f"Finished scraping {url}")


driver.close()
