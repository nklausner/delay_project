#!/usr/bin/env python3
# coding: utf-8


from os import listdir, path
import json


mydict = dict()
mydict['_all_'] = dict()
mydict['_all_']['trains'] = []


with open(path.join('data', 'zugfinder_example_stations.json'), 'r') as myfile:
    zugfinder_dict = json.loads(myfile.read())


def find_coordinates(mystation):
    for key in zugfinder_dict:
        if key == 'cities':
            break
        if zugfinder_dict[key]["name"] == mystation:
            return zugfinder_dict[key]['lat'], zugfinder_dict[key]['lon']
    print(mystation)
    return 0.0, 0.0


for myfilename in listdir(path.join('data', 'trains')):
    with open(path.join('data', 'trains', myfilename), 'r') as myfile:
        mytext = myfile.read()
        mylist = mytext.splitlines()[0].split(',')[1:]
        mytrain = myfilename[:-10]
        mydict['_all_']['trains'].append(mytrain)

        for s in mylist:
            if s in mydict:
                mydict[s]['trains'].append(mytrain)
            else:
                lat, lon = find_coordinates(s)
                mydict[s] = dict()
                mydict[s]['lat'] = lat
                mydict[s]['lon'] = lon
                mydict[s]['trains'] = [mytrain]


#for (key, value) in mydict.items():
#    print(key, value)


with open(path.join('data', 'stations.json'), 'w') as myfile:
    myfile.write(json.dumps(mydict))
    print('saved as', path.join('data', 'stations.json'))