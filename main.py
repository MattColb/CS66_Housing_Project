from dash import Dash, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
#import dbwork

app = Dash(__name__)

app.layout = html.Div(children = [
    dcc.Markdown(
        children = "Hello World"
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)