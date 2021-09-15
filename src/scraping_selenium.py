from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from credentials import myemail, mypass
import time
import pandas as pd


# https://www.zugfinder.net/js/zuginfo_json.php?z=ICE_555&d=2019-01-01

train_id = 'ICE_555'
url_login = 'https://www.zugfinder.net/en/login'
url_info = 'https://www.zugfinder.net/js/zuginfo_json.php?'
url_train = 'https://www.zugfinder.net/en/train-' + train_id
dates = pd.date_range("2019-01-01", "2019-02-28", freq="D")


myoptions = Options()
myoptions.headless = True
browser = webdriver.Firefox(options=myoptions)


browser.get(url_login)
input_email = browser.find_element_by_name("email")
input_pass = browser.find_element_by_name("pass")
input_email.send_keys(myemail)
input_pass.send_keys(mypass)
input_pass.send_keys(Keys.ENTER)
print(url_login)
time.sleep(5.0)


def click_bot_popup():
    """find normal page, cause popup and cofirm"""
    time.sleep(2.0)
    browser.get(url_train)
    time.sleep(2.0)
    my_tr = browser.find_element_by_id("2021-09-14")
    my_tr.find_element_by_tag_name("td").click()
    time.sleep(1.0)
    browser.find_element_by_link_text("Bitte bestätige, dass du ein Mensch bist!").click()
    time.sleep(1.0)
    browser.find_element_by_name("loesung").send_keys("8")
    time.sleep(1.0)
    browser.find_element_by_xpath('//*[@value="antworten"]').click()
    time.sleep(1.0)
    print(browser.find_element_by_id("detail").text)
    time.sleep(1.0)
    browser.find_element_by_class_name("closer").click()
    time.sleep(2.0)


count = 69
for d in dates:

    my_url = url_info + f'z={train_id}&d={d.date()}'
    my_path = f'data/{train_id}/{d.date()}.txt'
    try:
        browser.get(my_url)
        my_json = browser.find_element_by_id("json")
        f = open(my_path, "w")
        f.write(my_json.text)
        f.close()
        print(my_path)
    except:
        print(f'failed {d.date()}')
    count -= 1
    if count == 0:
        click_bot_popup()
        count = 69
    else:
        time.sleep(1.5)



browser.close()
#browser.quit()