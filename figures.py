import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from tools import evaluate_list_literal

def bay_fig(bay_data: pd.DataFrame, states_data: pd.DataFrame,
            state: str, rooms_list: 'list[int]') -> go.Figure:
    bay_fig = go.Figure(layout=go.Layout(
        xaxis={'title': 'Year'},
        yaxis={'title': 'Price', 'range': [0,5000]},
        title='Comparing Prices',
        height=1250
    ))

    for rooms in rooms_list:
        bay_fig.add_trace(go.Scatter(
            x=bay_data.index, y=bay_data[rooms],
            mode='lines+markers', name=f'bay{rooms}'
        ))

    def state_average() -> pd.DataFrame:
        years = states_data.columns[1:]
        temp = states_data.query(f"state_alpha == '{state}'")

        curr_prices = [[],[],[],[],[]]
        for year in years:
            vals = evaluate_list_literal(str(temp[year]))
            for n in range(5):
                curr_val = vals[n]
                curr_prices[n].append(curr_val)

        beds_df = pd.DataFrame(curr_prices, columns=years).transpose()
        return beds_df

    beds_df = state_average()
    for beds in rooms_list:
        bay_fig.add_trace(go.Scatter(
            x=beds_df.index, y=beds_df[beds],
            mode='markers', name=f'{state}{beds}'
        ))

    return bay_fig


def craigslist_all_fig(data: 'list[dict]') -> go.Figure:
    return px.scatter(data, x='date', y='price', color='county',
                      labels={'price': 'price ($)'})


def craigslist_avg_fig(data: 'list[dict]') -> go.Figure:
    return px.scatter(data, x='year', y='sqft_price',
                      color='county', trendline='ols',
                      labels={'sqft_price': 'price ($/sqft)'})


def homelessness_fig(data: pd.DataFrame,
                     graph_type: str,
                     start_year: int) -> go.Figure:
    COLORS = ["#004477", "#0070c4", "#0061aa", "#00355e", "#00182b"]
    filtered_data = data.query('Year >= @start_year')

    if graph_type == 'Correlation Graph':
        fig = px.scatter(filtered_data,
                         x='Median Rent',
                         y='Number of People Experiencing Homelessness',
                         trendline='ols', width=1000, height=500,
                         color_discrete_sequence=[COLORS[0]])
    elif graph_type == 'Median Rent vs. Number of People Experiencing Homelessness':
        fig = px.line(filtered_data, x='Year', y=data.columns[1:6],
                      width=1000, height=500,
                      color_discrete_sequence=COLORS)
        fig.update_layout(legend_orientation='h',
                          legend_yanchor='bottom',
                          legend_y=1.02,
                          legend_xanchor='right',
                          legend_x=1)
    else:
        fig = px.line(filtered_data, x='Year', y=graph_type,
                      width=1000, height=500,
                      color_discrete_sequence=[COLORS[0]])

    return fig
