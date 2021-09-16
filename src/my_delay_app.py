import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pydeck import Deck, Layer, ViewState
#from pydeck.bindings import view_state
import datetime
import os
import json


# set stuff
st.title('Train delays')
sns.set_theme(style="whitegrid", rc={'figure.figsize':(16,8)})


# load data
train_list = os.listdir(os.path.join('data','trains'))
train_list = [s[:-10] for s in train_list]
train_list = [s.replace('_', ' ') for s in train_list]
with open(os.path.join('data', 'stations.json'), 'r') as myfile:
    station_dict = json.loads(myfile.read())
#dfstations = pd.io.json.read_json(f'data/stations.json')


# station selection
searchstation = st.selectbox('show only trains stopping at', station_dict.keys(), index=0)
train_list = station_dict[searchstation]['trains']


# train selection
mytrain = st.selectbox('choose your train', train_list)
mystring = mytrain.replace(' ', '_')
df = pd.read_csv(f'data/trains/{mystring}_delay.csv', index_col=0, parse_dates=True)
station_list = list(df.columns)


# average delay graph
st.subheader(f'average delay of {mytrain}')
fig, ax = plt.subplots()
ax = sns.lineplot(data=df.mean(), color="red")
plt.ylim(0,20)
plt.yticks(fontsize=18)
plt.xticks(fontsize=18, rotation=45, horizontalalignment="right")
plt.ylabel('delay in minutes', fontsize=20)
st.write(fig)


# prepare coordinates
dfcoor = pd.DataFrame(index=station_list, columns=['lat', 'lon'])
for s in station_list:
    dfcoor.loc[s, 'lat'] = station_dict[s]['lat']
    dfcoor.loc[s, 'lon'] = station_dict[s]['lon']


# the map
view_state = ViewState(latitude=50.8, longitude=9.5, zoom=5)
train_layer = Layer('ScatterplotLayer',
    data=dfcoor,
    get_position=['lon', 'lat'],
    get_color='[204,0,0,204]',
    get_radius=8000)
st.pydeck_chart(Deck(
    map_style = 'mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[train_layer,]
))


# station selection
mystation = st.selectbox('choose your station', station_list)
myyear = st.selectbox('choose year', [2019, 2020, 2021], index=2)


# station delay graph
st.subheader(f'delay of {mytrain} in {mystation}')
fig1, ax1 = plt.subplots()
ax1 = df[mystation].plot(color='r')
plt.ylim(0,)
plt.xlim(datetime.date(myyear, 1, 1), datetime.date(myyear, 12, 31))
plt.ylabel('delay in minutes', fontsize=20)
plt.xlabel('')
plt.yticks(fontsize=18)
plt.xticks(fontsize=18)
st.write(fig1)


# prediction
st.subheader(f'delay of {mytrain} in {mystation}')
mydelays = list(df[mystation].dropna())
mydelays.sort()
n = 4
quartiles = [mydelays[i*len(mydelays)//n] for i in range(n)] + [mydelays[-1]]
quartile_ranges = [f'{int(quartiles[i])} - {int(quartiles[i+1])} minutes' for i in range(n)]
dfq = pd.DataFrame(data=quartile_ranges, index=[f'with {100//n} % chance' for i in range(n)], columns=['in the range of:'])
st.write(dfq)


