from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from credentials import myemail, mypass
import time

url_login = 'https://www.zugfinder.net/en/login'
url_train = 'https://www.zugfinder.net/js/zuginfo_json.php?'
train_id = 'EC_8'
month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

browser = webdriver.Firefox()

browser.get(url_login)
input_email = browser.find_element_by_name("email")
input_pass = browser.find_element_by_name("pass")
input_email.send_keys(myemail)
input_pass.send_keys(mypass)
input_pass.send_keys(Keys.ENTER)
print('log in')
time.sleep(5.0)


for year in [2019]:
    for month in [2,1]:
        for day in range(1, 1+month_days[month-1]):

            my_url = url_train + f'z={train_id}&d={year}-{month:02}-{day:02}'
            my_path = f'data/{train_id}/{year}-{month:02}-{day:02}.txt'
            try:
                browser.get(my_url)
                my_json = browser.find_element_by_id("json")
                if 'Zu viele Abfragen in zu kurzer Zeit' not in my_json.text:
                    f = open(my_path, "w")
                    f.write(my_json.text)
                    f.close()
                    print(my_path)
                else:
                    print('Zu viele Abfragen in zu kurzer Zeit')
                    break
            except:
                print(f'failed {year}-{month:02}-{day:02}')
            time.sleep(2.0)

#browser.close()
#browser.quit()