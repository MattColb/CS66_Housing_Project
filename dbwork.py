import pandas
import os

list_median = []

for file in os.listdir("./FY2001-2018-50-percentile/"):
    list_median.append([pandas.read_excel("./FY2001-2018-50-percentile/" +file), str(file[2:6])])

main_housing_data = pandas.read_csv("clean_2000_2018.csv")

homeless_data = pandas.read_csv("HSH_90_day_emergency_shelter_waitlist.csv")


def state_averages(state, year, rooms):
    for db in list_median:
        if db[1] == year:
            temp = db[0]
            temp[temp["state_alpha"] == state]
            for col in temp.columns:
                if len(col) >7 and col[6:8] == ("_" + rooms):
                    return int(temp[col].mean())

for db in range(len(list_median)):
    for col in list_median[db][0].columns:
        if not(col[4:6] == "50" or col[0:3] == "pop" or col == "state_alpha"  or col[0:2] == "hu" or col.lower() == "countyname"):
            list_median[db][0].drop(col, inplace=True, axis=1)

states_dictionary = {}

for state in list_median[0][0].state_alpha.unique():
    states_dictionary[state] = {}
    for year in list_median:
        states_dictionary[state][year[1]] = {}
        for room in range(5):
            states_dictionary[state][year[1]][str(room)] = state_averages(state, year[1], str(room))

def average_by_state(state):
    beds = [[],[],[],[],[]]
    years = states_dictionary[state].keys()
    for i in years:
        for rooms in range(5):
            beds[rooms].append(states_dictionary[state][i][str(rooms)])
    print(beds, years)


average_by_state("AL")