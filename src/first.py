import json

# status, stations, started, nextrun, train_nr, finished, date
# arrival, departure, station_id, delay, delay_cause, scraped

def print_station(s):
    name = stations[str(s["station_id"])]["name"].ljust(24)
    dep = "     "
    arr = "     "
    if "departure" in s:
        h = s['departure']//60
        m = s['departure']%60
        dep = f"{h:02}:{m:02}"
    if "arrival" in s:
        h = s['arrival']//60
        m = s['arrival']%60
        arr = f"{h:02}:{m:02}"
    delay = ""
    cause = ""
    if "delay" in s:
        delay = s["delay"]
    if "delay_cause" in s:
        cause = s["delay_cause"]
    print("-", name, arr, dep, delay, cause)


def print_train(t):
    print("")
    print(t['train_nr'], t['status'])
    print(t['date'], t['started'], t['finished'], t['nextrun'])
    for s in t['stations']:
        print_station(s)


with open('data/zugfinder_example_stations.json') as myfile:
    stations = json.load(myfile)

with open('data/zugfinder_example_trains.json') as myfile:
    trains = json.load(myfile)
    for i in trains:
        print_train(trains[i])