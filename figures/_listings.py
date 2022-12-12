import plotly.express as px
import plotly.graph_objects as go

def listings_fig(data: 'list[dict]') -> go.Figure:
    counties = {listing['county'] for listing in data}
    order = {'county': sorted(counties)}
    return px.scatter(data, x='date', y='price', color='county',
                      labels={'price': 'price ($)'},
                      title='Housing Prices in the Bay Area',
                      category_orders=order)