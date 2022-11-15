import pandas
import os

median_pricing = []

for file in os.listdir("./FY2001-2018-50-percentile/"):
    median_pricing.append(pandas.read_excel("./FY2001-2018-50-percentile/" +file))

main_housing_data = pandas.read_csv("clean_2000_2018.csv")

homeless_data = pandas.read_csv("HSH_90_day_emergency_shelter_waitlist.csv")

print(pandas.DataFrame.head(homeless_data))
print(pandas.DataFrame.head(main_housing_data))
