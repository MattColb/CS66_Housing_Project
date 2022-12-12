import pandas as pd
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