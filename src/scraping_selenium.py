#!/usr/bin/env python3
# coding: utf-8


from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from credentials import myemail, mypass
from time import sleep
from pandas import date_range
from sys import argv, exit
from os import mkdir, listdir


def make_train_directory(mytrain):
    """make subdirectory for given train"""
    try:
        mkdir(f'data/{mytrain}')
        print(f'created data/{mytrain}')
    except:
        pass


def find_missing_dates(mytrain):
    """compares files and dates and return list of missing files"""
    date_list = date_range("2019-01-01", "2021-09-12", freq="D")
    date_list = [f'{d.date()}' for d in date_list]
    file_list = listdir(f'data/{mytrain}')
    mylist = [d for d in date_list if f'{d}.txt' not in file_list]
    print(f'{len(mylist)} dates left')
    return mylist


def login_zugfinder(mybrowser):
    """login"""
    url_login = 'https://www.zugfinder.net/en/login'
    mybrowser.get(url_login)
    mybrowser.find_element_by_name("email").send_keys(myemail)
    mybrowser.find_element_by_name("pass").send_keys(mypass)
    mybrowser.find_element_by_name("pass").send_keys(Keys.ENTER)
    print(url_login)
    sleep(5.0)


def scrape_zugfinder(mybrowser, mytrain, mydates, count=69):
    """scrapes json files for given train and date list"""
    url_info = 'https://www.zugfinder.net/js/zuginfo_json.php?'
    count_success = 0
    count_failed = 0
    for d in mydates:

        my_url = url_info + f'z={mytrain}&d={d}'
        my_path = f'data/{mytrain}/{d}.txt'
        try:
            mybrowser.get(my_url)
            my_json = browser.find_element_by_id("json")
            f = open(my_path, "w")
            f.write(my_json.text)
            f.close()
            print(my_path)
            count_success += 1
        except:
            print(f'failed {d}')
            count_failed += 1
        count -= 1
        if count == 0:
            click_bot_popup(mybrowser, mytrain)
            count = 69
        else:
            sleep(1.0)
    print(f'this run: saved {count_success}, failed {count_failed}, count {count}')
    print('')
    return count


def click_bot_popup(mybrowser, mytrain):
    """find normal page, cause popup and cofirm"""
    url_train = 'https://www.zugfinder.net/en/train-' + mytrain
    sleep(2.0)
    mybrowser.get(url_train)
    sleep(2.0)
    my_tr = mybrowser.find_element_by_id("2021-09-14")
    my_tr.find_element_by_tag_name("td").click()
    sleep(1.0)
    mybrowser.find_element_by_link_text("Bitte bestätige, dass du ein Mensch bist!").click()
    sleep(1.0)
    mybrowser.find_element_by_name("loesung").send_keys("8")
    sleep(1.0)
    mybrowser.find_element_by_xpath('//*[@value="antworten"]').click()
    sleep(1.0)
    print(mybrowser.find_element_by_id("detail").text)
    sleep(1.0)
    mybrowser.find_element_by_class_name("closer").click()
    sleep(2.0)


if __name__ == '__main__':

    train_id = ''
    try:
        train_id = argv[1]
    except:
        print('specify train id')
        exit(1)
    make_train_directory(train_id)

    myoptions = Options()
    myoptions.headless = True
    browser = webdriver.Firefox(options=myoptions)
    login_zugfinder(browser)

    # main run
    date_list = find_missing_dates(train_id)
    c = scrape_zugfinder(browser, train_id, date_list)

    # try again
    date_list = find_missing_dates(train_id)
    c = scrape_zugfinder(browser, train_id, date_list, c)

    #important - browser.close() doesnt work here
    browser.quit() 

    # https://www.zugfinder.net/js/zuginfo_json.php?z=ICE_555&d=2019-01-01
