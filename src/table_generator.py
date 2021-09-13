#!/usr/bin/env python3
# coding: utf-8


import os
import pandas as pd
import numpy as np
from ast import literal_eval


def read_data(my_file_list, my_date_list):
    """collects content of files in a list, add dummys if missing"""
    print('reading data')
    mydata = []
    for datetime in my_date_list:
        filename = str(datetime.date()) + '.txt'
        if filename in my_file_list:
            with open(os.path.join('data', train_id, filename), 'r') as myfile:
                mystr = myfile.read()
                if len(mystr) > 0:
                    mylist = literal_eval(mystr)
                    mydata.append(mylist)
                else:
                    mydata.append([])
        else:
            mydata.append([])
    return mydata


def create_route_dictionary(mydata):
    """collects routes and count their occurence"""
    print('finding routes')
    mydict = dict()
    for mylist in mydata:
        s = ""
        for entry in mylist:
            if isinstance(entry, dict):
                s += '_' + entry['bhf']
        s = s[1:]
        if s in mydict:
            mydict[s] += 1
        else:
            mydict[s] = 1
    return mydict


train_id = 'EC_8'
file_list = os.listdir(os.path.join('data', train_id))
file_list.sort()
summary = file_list.pop(-1)
date_start = os.path.splitext(file_list[0])[0]
date_final = os.path.splitext(file_list[-1])[0]
datetime_index = pd.date_range(date_start, date_final, freq="D")


data = read_data(file_list, datetime_index)
route_dict = create_route_dictionary(data)
main_route = max(route_dict, key=route_dict.get)
main_route = main_route.split('_')
print(main_route)


width = 2 * len(main_route)
height = len(datetime_index)
my_array = np.full(shape=(height, width), fill_value=np.nan)


print('filling array')
for y in range(height):
    for s in data[y]:
        if isinstance(s, dict) and s['bhf'] in main_route:
            x = 2 * main_route.index(s['bhf'])
            ad = int(s['adelay'])
            if ad >= 0:
                my_array[y][x] = ad
            dd = int(s['ddelay'])
            if dd >= 0:
                my_array[y][x+1] = dd

column_names = []
for station in main_route:
    column_names.append(station + '_ad')
    column_names.append(station + '_dd')


df = pd.DataFrame(data=my_array, index=datetime_index, columns=column_names)
df.to_csv(f'data/{train_id}_delay.csv')
print(f'saved to data/{train_id}_delay.csv')
#print(df)

