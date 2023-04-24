import dash
import dash_bootstrap_components as dbc
from dash import dcc, callback, Output, Input
from dash import html
import pandas as pd
from dash import dash_table

import plotly.express as px

from GetStaticticDF import statistic_table, table_for_time_line_graf, family_history_table

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
FullTable = statistic_table()
TimeLineStat = table_for_time_line_graf(FullTable)
FamilyHistoryTable = family_history_table()
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

    html.H3(children='Число внесенных изменений от Bim-специалистов', style={'textAlign': 'center'}),
    dcc.Graph(
        id='FamilyHistory',
        figure={
            'data': [
                {'x': FamilyHistoryTable['Creater'], 'type': 'histogram'}
            ],
        }
    ),

    html.H3(children='Количество использованных команд пользователем', style={'textAlign': 'center'}),
    dcc.Graph(
        id='FamilyHistory',
        figure={
            'data': [
                {'x': FullTable['UserName'], 'type': 'histogram'},

            ],
        }
    ),

    html.H3(children='Количество использованных команд по проектам', style={'textAlign': 'center'}),
    dcc.Graph(
        id='FamilyHistory',
        style={'margin-bottom': 10},
        figure={

            'data': [
                {'x': FullTable['Project'], 'type': 'histogram'}
            ],
            'layout': {'height': 800},
        },
    ),

    html.H3(children='⠀', style={'textAlign': 'center'}),
    html.H3(children='Динамика использования команд', style={'textAlign': 'center'}),
    html.H3(children='⠀', style={'textAlign': 'center'}),
    dash_table.DataTable(TimeLineStat.to_dict('records'), [{"name": i, "id": i} for i in TimeLineStat.columns]),

    html.H3(children='⠀', style={'textAlign': 'center'}),
    html.H3(children='График использования на временной линии', style={'textAlign': 'center'}),
    dcc.Graph(
        id='UseAllComandInTimeLine',
        figure={
            'data': [
                {'x': TimeLineStat[TimeLineStat['Имя команды'] == 'Загрузить выбранные типы']['Дата'].tolist(),
                 'y': TimeLineStat[TimeLineStat['Имя команды'] == 'Загрузить выбранные типы']['Число использований'].tolist(),
                 'type': 'histogram', 'name': 'Загрузить выбранные типы'},

                {'x': TimeLineStat[TimeLineStat['Имя команды'] == 'Разместить эл-т']['Дата'].tolist(),
                 'y': TimeLineStat[TimeLineStat['Имя команды'] == 'Разместить эл-т'][
                     'Число использований'].tolist(),
                 'type': 'histogram', 'name': 'Разместить эл-т'},
            ],
        }
    ),

    html.H3(children='⠀', style={'textAlign': 'center'}),
    html.H3(children='График использования команд на временной линии', style={'textAlign': 'center'}),
    html.H3(children='⠀', style={'textAlign': 'center'}),
    dcc.Dropdown(TimeLineStat['Имя команды'].unique(), 'Загрузить выбранные типы', id='dropdown-selection'),
    dcc.Graph(id='graph-content'),
])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'))
def update_graph(value):
    dff = TimeLineStat[FullTable['Имя команды'] == value]
    return px.line(dff, x='Дата', y='Число использований')


if __name__ == '__main__':
    print(TimeLineStat[TimeLineStat['Имя команды'] == 'Загрузить выбранные типы']['Дата'].tolist())
    print(TimeLineStat[TimeLineStat['Имя команды'] == 'Загрузить выбранные типы']['Число использований'].tolist())
    app.run_server(debug=True)

