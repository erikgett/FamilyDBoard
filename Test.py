from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

dff = pd.DataFrame(dict(
    x=[1, 3, 2, 4],
    y=[1, 2, 3, 4]
))

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
    dcc.Dropdown(dff.x.unique(), '1', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])


@callback(Output('graph-content', 'figure'), Input('dropdown-selection', 'value'))
def update_graph(value):
    return px.line(dff, x="x", y="y")


if __name__ == '__main__':
    app.run_server(debug=True)
