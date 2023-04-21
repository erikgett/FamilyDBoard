import dash
import dash_bootstrap_components as dbc
from dash import dcc, callback, Output, Input
from dash import html
import pandas as pd

import plotly.express as px

from GetStaticticDF import statistic_table, table_for_time_line_graf

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
FullTable = statistic_table()
TimeLineStat = table_for_time_line_graf(FullTable)
app.layout = html.Div([
    html.H3(children='График использования команд', style={'textAlign': 'center'}),
    dcc.Graph(
        id='CommandClicked',
        figure={
            'data': [
                {'x': FullTable['Имя команды'], 'type': 'histogram'}
            ],
        }
    ),
    html.H3(children='График использования команд на временной линии', style={'textAlign': 'center'}),
    dcc.Dropdown(TimeLineStat['Имя команды'].unique()[1:], 'Разместить эл-т', id='dropdown-selection'),
    dcc.Graph(id='graph-content'),
    html.H3(children='Число внесенных изменений от Bim-специалистов', style={'textAlign': 'center'}),
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'))
def update_graph(value):
    dff = TimeLineStat[FullTable['Имя команды'] == value]
    return px.line(dff, x='Дата', y='Имя команды')

if __name__ == '__main__':
    app.run_server(debug=True)
