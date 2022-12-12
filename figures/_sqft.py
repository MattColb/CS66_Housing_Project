import plotly.express as px
import plotly.graph_objects as go

def sqft_fig(data: 'list[dict]') -> go.Figure:
    counties = {listing['county'] for listing in data}
    order = {'county': sorted(counties)}
    return px.scatter(data, x='year', y='sqft_price',
                      color='county', trendline='ols',
                      labels={'sqft_price': 'price ($/sqft)'},
                      title='Average Prices by Year',
                      category_orders=order)