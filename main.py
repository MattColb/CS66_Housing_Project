from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from figures import bay_fig, homelessness_fig, listings_fig, sqft_fig
from load_data import (load_beds_data, load_listings_data,
                       load_homelessness_data, load_sqft_data,
                       load_states_data)
from tools import find_correlation


BAY_ALL_PATH = 'data/all_bay_data.json'
BEDS_DATA_PATH = 'data/beds_data.csv'
HOMELESSNESS_DATA_PATH = 'data/homelessness_data.csv'
STATES_DATA_PATH = 'data/national_data.csv'
SQFT_DATA_PATH = 'data/sqft_data.json'


if __name__ == '__main__':
    listings = load_listings_data(BAY_ALL_PATH)
    beds_df = load_beds_data(BEDS_DATA_PATH)
    homelessness_df = load_homelessness_data(HOMELESSNESS_DATA_PATH)
    states_df = load_states_data(STATES_DATA_PATH)
    sqft_data = load_sqft_data(SQFT_DATA_PATH)

    correlation = find_correlation(
        homelessness_df,
        'Median Rent',
        'Number of People Experiencing Homelessness'
    )
    recent_correlation = find_correlation(
        homelessness_df.loc[homelessness_df['Year'] >= 2014],
        'Median Rent',
        'Number of People Experiencing Homelessness'
    )

    craigslist_all_fig = listings_fig(listings)
    craigslist_avg_fig = sqft_fig(sqft_data)

    app = Dash(__name__)

    @app.callback(
        Output(component_id='correlation_fig', component_property='figure'),
        [Input(component_id='dropdown', component_property='value'),
         Input(component_id='my-slider', component_property='value')]
    )
    def get_homelessness_fig(dropdown_value, slider_value):
        return homelessness_fig(homelessness_df, dropdown_value, slider_value)

    @app.callback(
        Output(component_id='bay_fig', component_property='figure'),
        [Input(component_id='state', component_property='value'),
         Input(component_id='rooms_check', component_property='value')]
    )
    def get_bay_fig(state, rooms_checked):
        return bay_fig(beds_df, states_df, state, rooms_checked)

    app.layout = html.Div(
        id='parent',
        style={
            'color': '#004477',
            'font-family': 'Arial'
        },
        children=[
            html.H2(
                id='H1',
                children='Median Rent vs. People Experiencing Homelessness',
                style={'textAlign': 'center'}
            ),
            dcc.Slider(
                min=2007,
                max=2017,
                step=None,
                id='my-slider',
                marks={year: str(year) for year in range(2007, 2018)},
                value=2007
            ),
            dcc.Dropdown(
                id='dropdown',
                options=[
                    'Correlation Graph',
                    'Median Rent vs. Number of People Experiencing Homelessness',
                    'Number of People Experiencing Homelessness',
                    'Families',
                    'Unsheltered',
                    'Sheltered'
                ],
                value='Median Rent vs. Number of People Experiencing Homelessness',
                clearable=False,
                style={
                    'float': 'left',
                    'width': '70%'
                }
            ),
            dcc.Graph(
                id='correlation_fig',
                figure=get_homelessness_fig(
                    'Median Rent vs. Number of People Experiencing Homelessness',
                    2007
                ),
                style={
                    'float': 'left',
                    'display': 'inline-block'
                }
            ),
            dcc.Markdown(
                id='correlation_val',
                children=[
                    'Median rent and the number of people\n',
                    'experiencing homelessness in San\n',
                    'Francisco are strongly positively\n',
                    'correlated. The correlation coefficient\n',
                    f'is {round(correlation, 2)}, and it has increased\n',
                    f'to {round(recent_correlation, 2)} since 2014.'
                ],
                style={
                    'float': 'right',
                    'display': 'inline-block',
                    'font-family':'Arial'
                }
            ),
            html.H2(
                children='Median Housing Prices in Bay Area vs Average Median Housing Counties per State by County',
                style={
                    'clear': 'both',
                    'textAlign': 'center'
                }
            ),
            dcc.Dropdown(
                id='state',
                options=states_df.state_alpha.unique(),
                value = 'US'
            ),
            dcc.Markdown(
                children='Number of Rooms'
            ),
            dcc.Checklist(
                id='rooms_check',
                options=[*range(5)],
                value=[*range(5)]
            ),
            dcc.Graph(
                id='bay_fig',
                figure=get_bay_fig('US', [*range(5)])
            ),
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

    app.run(debug=True)