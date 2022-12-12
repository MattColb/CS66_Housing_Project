import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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