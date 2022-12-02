import pandas as pd
import numpy as np
import os

list_median = []
main_housing_data = pd.read_csv("clean_2000_2018.csv")

for file in os.listdir("./FY2001-2018-50-percentile/"):
    list_median.append([pd.read_excel("./FY2001-2018-50-percentile/" +file), str(file[2:6])])

def read_homeless_data():
    homeless_data = pd.read_csv("HSH_90_day_emergency_shelter_waitlist.csv")
    return homeless_data

"""Start of Matt's Code"""
#Column names that consist of all the years, and the state_alphas, which are used for the 
colnames=["state_alpha"]
for year in list_median:
    colnames.append(year[1])

#Cleaning the data and handling the type issues in the beds column
compare_to_states = main_housing_data[["year", "price", "beds"]]
compare_to_states = compare_to_states.dropna()
for values in list(compare_to_states.beds.unique()):
    if type(values) == float:
        compare_to_states = compare_to_states.replace(values, str(int(values)))

#Filtering out the different columns in all of the medians data sets. 
for db in range(len(list_median)):
    for col in list_median[db][0].columns:
        if not(col[4:6] == "50" or col[0:3] == "pop" or col == "state_alpha"  or col[0:2] == "hu" or col.lower() == "countyname"):
            list_median[db][0].drop(col, inplace=True, axis=1)

#Calculating the list of all states and handling the na that is in the list
states_list = list_median[0][0].state_alpha.unique()
states_list = np.delete(states_list, 51)
states_list = np.append(states_list, "national_averages")

#Calculate the median for each combination of year and rooms
def bay_averages(year, rooms):
    temp = compare_to_states
    temp = temp.dropna()
    temp = temp.loc[(temp["year"] == int(year)) & (temp["beds"] == str(rooms))] 
    return pd.to_numeric(temp["price"].median()) #Median here would be most like the 50th percentile that is present in what I am comparing it to.

#Calculating the averages based upon State, year, and room. This also works for national averages as it ignores the filtering
def state_averages(state, year, rooms):
    for db in list_median:
        if db[1] == year:
            temp = db[0]
            temp = temp.dropna()
            if state != None:
                temp = temp.loc[temp["state_alpha"] == state]
            for col in temp.columns:
                if len(col) >7 and col[6:8] == ("_" + rooms):
                    return int(pd.to_numeric(temp[col].mean()))

def creating_dbs():
    #Creating a list with all combinations of years and rooms to create a dataframe for the bay area pricing
    bay_pricing = []
    for rooms in range(5):
        curr_prices = []
        for year in colnames[1:]:
            price = bay_averages(year, rooms)
            curr_prices.append(int(price))
        bay_pricing.append(curr_prices)
    bay_df = pd.DataFrame(bay_pricing, columns=colnames[1:])

    #Creating a list with all combinations of states, years, and rooms to create a dataframe for the median pricing over the years by state
    states_pricing = []
    for state in range(len(states_list)-1):
        states_pricing.append([states_list[state]])
        for year in list_median:
            curr_prices = []
            for room in range(5):
                price = state_averages(states_list[state], year[1], str(room))
                curr_prices.append(price)
            states_pricing[state].append(curr_prices)
    #Creating a list with all combinations of years and rooms to create a dataframe for the median pricing over the years in the nation
    national_pricing = ["national_averages"]
    for year in list_median:
        curr_prices = []
        for room in range(5):
            price = state_averages(None, year[1], str(room))
            curr_prices.append(price)
        national_pricing.append(curr_prices)
    states_pricing.append(national_pricing)
    states_df = pd.DataFrame(states_pricing, columns=colnames)
    return bay_df, states_df

#Handling the unique nature of the states data frame being 3 dimensional
def average_by_state(states_df, state):
    years = colnames[1:]
    temp = states_df
    temp = temp.loc[temp["state_alpha"] == state]
    curr_prices = [[],[],[],[],[]]
    for i in years:
        vals = str(temp[i]).split("[")[1].split(']')[0].split(",")
        for n in range(5):
            curr_val = vals[n]
            curr_prices[n].append(curr_val)
    beds_df = pd.DataFrame(curr_prices, columns=years)
    beds_df = beds_df.T
    return beds_df

#Decided to export the data instead of having it run on each startup of the plotly to reduce time. If update is needed, just run this function again.
def exporting_dfs():
    bay_df, states_df = creating_dbs()
    bay_df.to_csv(r'./ComparisonOut/bay_df.csv', index=True)
    states_df.to_csv(r'./ComparisonOut/states_df.csv')

"""End of Matt's Code"""