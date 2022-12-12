from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import dbwork
import math
import datetime
import json


def formatted_date(date):
    year, month, day = date[:4], date[4:6], date[6:]
    return datetime.date(int(year), int(month), int(day))

def load_listings_data(path):
    with open(path, mode='r') as file:
        data = json.load(file)

    # Replace date strings with datetime objects.
    for listing in data:
        listing['date'] = formatted_date(listing['date'])

    return data

def load_sqft_data(path):
    with open(path, mode='r') as file:
        return json.load(file)

def listings_fig(data):
    counties = {listing['county'] for listing in data}
    order = {'county': sorted(counties)}
    return px.scatter(data, x='date', y='price', color='county',
                      labels={'price': 'price ($)'},
                      title='Housing Prices in the Bay Area',
                      category_orders=order)

def sqft_fig(data):
    counties = {listing['county'] for listing in data}
    order = {'county': sorted(counties)}
    return px.scatter(data, x='year', y='sqft_price',
                      color='county', trendline='ols',
                      labels={'sqft_price': 'price ($/sqft)'},
                      title='Average Prices by Year',
                      category_orders=order)

listings = load_listings_data('all_bay_data.json')
sqft_data = load_sqft_data('sqft_data.json')

craigslist_all_fig = listings_fig(listings)
craigslist_avg_fig = sqft_fig(sqft_data)

app = Dash(__name__)

"""Matt Section"""
bay_df = pd.read_csv("./ComparisonOut/bay_df.csv")
bay_df = bay_df.drop("Unnamed: 0", axis=1)
bay_df = bay_df.T
states_df = pd.read_csv("./ComparisonOut/states_df.csv")
states_df = states_df.drop("Unnamed: 0", axis=1)

#Learned graph objects and layout using: https://www.programcreek.com/python/example/103216/plotly.graph_objs.Layout
bay_fig = go.Figure()
"""End Matt Section"""

"""Shelter Insecurity Figure by Blythe"""
df=pd.read_csv('Group Data Homeless.csv')

#Obtaining statistical data from the OLS trendline
fig = px.scatter(df, x='Median Rent', y='Number of People Experiencing Homelessness', trendline="ols", width=1000, height=500, color_discrete_sequence=["#004477"])
model = px.get_trendline_results(fig)
results = model.iloc[0]["px_fit_results"]
r_squared = results.rsquared

recentdf=df.loc[df['Year']>=2014]
fig = px.scatter(recentdf, x='Median Rent', y='Number of People Experiencing Homelessness', trendline="ols", width=1000, height=500, color_discrete_sequence=["#004477"])
model = px.get_trendline_results(fig)
results = model.iloc[0]["px_fit_results"]
recent_r_squared = results.rsquared

#Configuring app layout  
app.layout = html.Div(id = 'parent', 
style={'color': '#004477', 'font-family':'Arial'}, 
children = [
        html.H1(id = 'H1', 
        children = 'Median Rent vs. People Experiencing Homelessness', 
        style = {'textAlign':'center'}),

        dcc.Slider(2007, 2017,
        step=None, id='my-slider',
        marks={
            2007:'2007',
            2008:'2008',
            2009:'2009',
            2010:'2010',
            2011:'2011',
            2012:'2012',
            2013:'2013',
            2014:'2014',
            2015:'2015',
            2016:'2016',
            2017:'2017'
        },
        value=2007),

        dcc.Dropdown(id='dropdown',
        options=["Median Rent vs. Number of People Experiencing Homelessness",
        "Correlation Graph", 
        "Number of People Experiencing Homelessness", 
        "Families", 
        "Unsheltered",
        "Sheltered"],

        value="Median Rent vs. Number of People Experiencing Homelessness",
        style={'float': 'left', "width": "70%"}
        ),

        dcc.Graph(id = 'correlation_fig',
        className='dcc_compon',
        style={'float': 'left','display': 'inline-block'},
        ),
        
        dcc.Markdown(id="correlation_val",

        #displaying the statistical data next to the Plotly graph
        children=["Median rent and the number of people\n", "experiencing homelessness in San\n", "Francisco are strongly positively\n", "correlated. The correlation coefficient\n",
        "is {:.2f}, ".format(math.sqrt(r_squared))+"and it has increased\n", "to {:.2f} ".format(math.sqrt(recent_r_squared),) +" since 2014."],

        style={'float': 'right', 'display': 'inline-block', 'font-family':'Arial'}),

        #Matt Section
        html.H1(children="Median Housing Prices in Bay Area vs Average Median Housing Counties per State by County", style={"clear":"both", "textAlign":"center"}),

        dcc.Dropdown(id="state",options=dbwork.states_list, value = "national_averages"),

        dcc.Markdown(children="Number of Rooms"),

        dcc.Checklist(id="rooms_check", options=[0,1,2,3,4], value=[0,1,2,3,4]),

        dcc.Graph(id="bay_fig", figure=bay_fig),
        #End Matt Section
        
        html.H2('Craigslist Data'),
            dcc.Graph(
                id='craigslist-all-graph',
                figure=craigslist_all_fig
            ),
            dcc.Graph(
                id='average-graph',
                figure=craigslist_avg_fig
            )
])

@app.callback(Output(component_id='correlation_fig', component_property= 'figure'),
            [Input(component_id='dropdown', component_property= 'value'),
            Input(component_id='my-slider', component_property= 'value')])

def displaycorrelationfig(dropdown_value, slider_value):
    fig = px.line(data_frame=df, x='Year', y=df.columns[1:6], width=1000, height=500, color_discrete_sequence=["#004477", "#0070c4", "#0061aa", "#00355e", "#00182b"])
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1))

    if dropdown_value=="Correlation Graph":
        newdf=df.loc[df['Year']>=slider_value]
        fig = px.scatter(newdf, x='Median Rent', y='Number of People Experiencing Homelessness', trendline="ols", width=1000, height=500,  color_discrete_sequence=["#004477"])
        results = px.get_trendline_results(fig)
    elif dropdown_value=="Median Rent vs. Number of People Experiencing Homelessness":
        newdf=df.loc[df['Year']>=slider_value]
        fig = px.line(data_frame=newdf, x='Year', y=df.columns[1:6], width=1000, height=500, color_discrete_sequence=["#004477", "#0070c4", "#0061aa", "#00355e", "#00182b"])
        fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1))
    else:
        newdf=df.loc[df['Year']>=slider_value]
        fig = px.line(newdf, x='Year', y='{}'.format(dropdown_value), color_discrete_sequence=["#004477"])   

    return fig

"""Matt Colbert Section"""
@app.callback(Output(component_id="bay_fig", component_property="figure"),
                    [Input(component_id="state", component_property="value"),
                    Input(component_id="rooms_check", component_property="value")])

def display_bay_fig(state, rooms):
    beds_df = dbwork.average_by_state(states_df, state)
    bay_fig=go.Figure(layout=go.Layout(xaxis=dict(title="Year"), yaxis=dict(title="Price", range=[0,5000]), title="Comparing Prices", height=1250))
    for i in bay_df.columns[rooms]:
        bay_fig.add_trace(go.Scatter(x=bay_df.index, y=bay_df[i], mode="lines+markers", name="bay" + str(i)))
    for n in beds_df.columns[rooms]:
        bay_fig.add_trace(go.Scatter(x=beds_df.index, y=beds_df[n], mode="lines+markers", name=state+str(n)))
    return bay_fig

"""Matt Colbert Section End"""

if __name__ == '__main__':
    app.run_server(debug=True)
   
"""End of Blythe's code"""
