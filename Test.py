from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd


app = Dash(__name__)

from dash import dcc

app.layout = html.Div([
dcc.Graph(
    figure={
        'data': [
            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
        ],
        'layout': {
            'title': 'Dash Data Visualization'
        }
    }
)])

if __name__ == '__main__':
    app.run_server(debug=True)