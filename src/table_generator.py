#!/usr/bin/env python3
# coding: utf-8


import os
import pandas as pd
import numpy as np
from ast import literal_eval
from sys import argv, exit


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


def create_dataframe(mydata, mydates, myroute):
    """creates numpy array of needed dimension and fills it, returns dataframe"""
    print('creating array')
    w = len(myroute)
    h = len(mydates)
    myarray = np.full(shape=(h, w), fill_value=np.nan)
    for y in range(h):
        for s in mydata[y]:
            if isinstance(s, dict) and s['bhf'] in myroute:
                x = myroute.index(s['bhf'])
                ad = -1
                dd = -1
                if s['adelay']:
                    ad = int(s['adelay'])
                if s['ddelay']:
                    dd = int(s['ddelay'])
                if max(ad, dd) >= 0:
                    myarray[y][x] = max(ad, dd)
    return pd.DataFrame(data=myarray, index=mydates, columns=myroute)


if __name__ == '__main__':
    train_id = ''
    try:
        train_id = argv[1]
    except:
        print('specify train id')
        exit(1)

    file_list = []
    try:
        file_list = os.listdir(os.path.join('data', train_id))
    except:
        print(f'no such directory: data/{train_id}')
        exit(1)
    
    # preparing files and dates
    file_list.sort()
    summary = file_list.pop(-1)
    date_start = os.path.splitext(file_list[0])[0]
    date_final = os.path.splitext(file_list[-1])[0]
    datetime_index = pd.date_range(date_start, date_final, freq="D")

    # find the main route
    data = read_data(file_list, datetime_index)
    route_dict = create_route_dictionary(data)
    main_route = max(route_dict, key=route_dict.get)
    main_route_count = route_dict[main_route]
    main_route = main_route.split('_')
    print(main_route_count)
    print(main_route)

    # save dataframe as csv
    df = create_dataframe(data, datetime_index, main_route)
    df.index.name = 'date'
    df.to_csv(f'data/trains/{train_id}_delay.csv')
    print(f'saved to data/trains/{train_id}_delay.csv')
    #print(df)

