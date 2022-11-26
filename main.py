from dash import Dash, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd


app = Dash(__name__)


"""Shelter Insecurity Figure by Blythe"""
df=pd.read_csv('Group Data Homeless.csv')

newdf=df.loc[df['Year']>=2014]
fig = px.scatter(newdf, x='Median Rent', y='Number of People Experiencing Homelessness', trendline="ols", width=1000, height=500, color_discrete_sequence=["#004477"])
model = px.get_trendline_results(fig)

results = model.iloc[0]["px_fit_results"]
alpha = results.params[0]
beta = results.params[1]
p_beta = results.pvalues[1]
r_squared = results.rsquared
    
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

        children=["The correlation between median rent\n", "and the number of people experiencing\n", "homelessness in San Francisco is strong.\n",
        "R-squared value= {:.2f}".format(r_squared), "since 2014."],

        style={'float': 'right', 'display': 'inline-block', 'font-family':'Arial'})
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

if __name__ == '__main__':
    app.run_server(debug=True)
