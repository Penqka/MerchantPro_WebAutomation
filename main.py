from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re
import json


def connect_to_category(category, name):
    product.find_element("id", f"chk-{product_id[0]}").click()
    drop_down_btns = driver.find_elements(By.CLASS_NAME, "dropdown")
    for btn in drop_down_btns:
        if category in btn.get_attribute("innerHTML"):
            btn.click()
            options = driver.find_elements("xpath", "//li")

            for option in options:
                if category in option.get_attribute("innerHTML"):
                    option.click()
                    time.sleep(4)

                    dropdown_menu = driver.find_element("id", "form_fk_shop_cat").send_keys(name)
                    time.sleep(4)
                    driver.find_element("name", "btn_submit").click()


options = Options()
options.add_experimental_option("detach", True)

# start browser and log in
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("--website--")
driver.maximize_window()

username = "user"
password = "pass"

driver.find_element("id", "logins_ident").send_keys(username)
driver.find_element("id", "logins_password").send_keys(password)
driver.find_element("id", "btn_submit").click()

# navigate
prod_listing = "--website--"
driver.get(prod_listing)
main_category = "Свържи с категория"
secondary_category = "Свържи с допълнителна категория"

# find products
with open("CATEGORIES_DICT.json", encoding="utf8") as file:
    PHONE_BRAND_MODEL = json.load(file)

products = driver.find_elements("xpath", "//tr[@id]")

for product in products:
    name_pattern = r"\d+\">(.+)<\/a>"
    id_pattern = r'id="chk-(\d+)"'
    product_id = re.findall(id_pattern, product.get_attribute("innerHTML"))
    product_name, *data = re.findall(name_pattern, product.get_attribute("innerHTML"))

    for brand in PHONE_BRAND_MODEL.keys():

        try:
            if brand.upper() in product_name.upper():
                found_models = []

                for model in PHONE_BRAND_MODEL[brand]:
                    if model.upper() in product_name.upper():
                        found_models.append(model)

                if len(found_models) > 1:
                    for i in range(len(found_models) - 2, -1, -1):
                        name = brand + found_models.pop()
                        connect_to_category(secondary_category, name)

                name = brand + found_models.pop()
                connect_to_category(main_category, name)

                print(f"ID:{product_id}")
                print(f"NAME:{product_name}")
                print(f"FOUND MODELS:{found_models}")
                print()
                break

        except IndexError:
            pass
