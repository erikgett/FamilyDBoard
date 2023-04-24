import dash
import dash_bootstrap_components as dbc
from dash import dcc, callback, Output, Input
from dash import html
import pandas as pd
from dash import dash_table

import plotly.express as px

from GetStaticticDF import statistic_table, table_for_time_line_graf, family_history_table

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])
FullTable = statistic_table()
TimeLineStat = table_for_time_line_graf(FullTable)
FamilyHistoryTable = family_history_table()


app.layout = html.Div([
    html.Div(
        children=[
            html.P(children="🏢", className="header-emoji"),
            html.H1(children="Менеджер семейств", className="header-title"),
            html.P(
                children="Аналитика использования менеджера семейств\n"
                         "Первая часть - активность проектировщиков\n"
                         "Вторая часть - активность BIM-специалистов\n",
                className="header-description",
            )
        ],
        className="header",
    ),

    html.P(
        children="Аналитика использования менеджера семейств\n"
                 "Первая часть - активность проектировщиков\n"
                 "Вторая часть - активность BIM-специалистов\n",
        className="header-description",
    ),

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
        id='FamilyHistory1',
        figure={
            'data': [
                {'x': FullTable['UserName'], 'type': 'histogram'},

            ],
        }
    ),

    html.H3(children='Количество использованных команд по проектам', style={'textAlign': 'center'}),
    dcc.Graph(
        id='FamilyHistory2',
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
                {'x': TimeLineStat[TimeLineStat['Имя команды'] == 'Разместить эл-т']['Дата'].tolist(),
                 'y': TimeLineStat[TimeLineStat['Имя команды'] == 'Разместить эл-т']['Число использований'].tolist(),
                 'type': 'bar', 'name': 'Разместить эл-т'},

                {'x': TimeLineStat[TimeLineStat['Имя команды'] == 'Обновить все сем-ва']['Дата'].tolist(),
                 'y': TimeLineStat[TimeLineStat['Имя команды'] == 'Обновить все сем-ва']
                 ['Число использований'].tolist(), 'type': 'bar', 'name': 'Обновить все сем-ва'},

                {'x': TimeLineStat[TimeLineStat['Имя команды'] == 'Загрузить материалы']['Дата'].tolist(),
                 'y': TimeLineStat[TimeLineStat['Имя команды'] == 'Загрузить материалы']
                 ['Число использований'].tolist(), 'type': 'bar', 'name': 'Загрузить материалы'},

                {'x': TimeLineStat[TimeLineStat['Имя команды'] == 'Выбрать типы и загрузить']['Дата'].tolist(),
                 'y': TimeLineStat[TimeLineStat['Имя команды'] == 'Выбрать типы и загрузить']
                 ['Число использований'].tolist(), 'type': 'bar', 'name': 'Выбрать типы и загрузить'},

                {'x': TimeLineStat[TimeLineStat['Имя команды'] == 'Выделить все типы сем-ва']['Дата'].tolist(),
                 'y': TimeLineStat[TimeLineStat['Имя команды'] == 'Выделить все типы сем-ва']
                 ['Число использований'].tolist(), 'type': 'bar', 'name': 'Выделить все типы сем-ва'},

                {'x': TimeLineStat[TimeLineStat['Имя команды'] == 'Выделить все типы сем-ва на виде']['Дата'].tolist(),
                 'y': TimeLineStat[TimeLineStat['Имя команды'] == 'Выделить все типы сем-ва на виде']
                 ['Число использований'].tolist(), 'type': 'bar', 'name': 'Выделить все типы сем-ва на виде'},

                {'x': TimeLineStat[TimeLineStat['Имя команды'] == 'Выделить тип в проекте']['Дата'].tolist(),
                 'y': TimeLineStat[TimeLineStat['Имя команды'] == 'Выделить тип в проекте']
                 ['Число использований'].tolist(), 'type': 'bar', 'name': 'Выделить тип в проекте'},

                {'x': TimeLineStat[TimeLineStat['Имя команды'] == 'Выделить тип на виде']['Дата'].tolist(),
                 'y': TimeLineStat[TimeLineStat['Имя команды'] == 'Выделить тип на виде']
                 ['Число использований'].tolist(), 'type': 'bar', 'name': 'Выделить тип на виде'},

                {'x': TimeLineStat[TimeLineStat['Имя команды'] == 'Обновить сем-во']['Дата'].tolist(),
                 'y': TimeLineStat[TimeLineStat['Имя команды'] == 'Обновить сем-во']['Число использований'].tolist(),
                 'type': 'bar', 'name': 'Обновить сем-во'},

                {'x': TimeLineStat[TimeLineStat['Имя команды'] == 'Загрузить выбранные типы']['Дата'].tolist(),
                 'y': TimeLineStat[TimeLineStat['Имя команды'] == 'Загрузить выбранные типы']
                 ['Число использований'].tolist(), 'type': 'bar', 'name': 'Загрузить выбранные типы'},
            ],
        }
    ),

    html.H3(children='⠀', style={'textAlign': 'center'}),
    html.H3(children='График использования команд на временной линии', style={'textAlign': 'center'}),
    html.H3(children='⠀', style={'textAlign': 'center'}),
    dcc.Dropdown(TimeLineStat['Имя команды'].unique(), TimeLineStat['Имя команды'].unique()[0],
                 id='dropdown-selection'), dcc.Graph(id='graph-content')
])


@callback(Output('graph-content', 'figure'), Input('dropdown-selection', 'value'))
def update_graph(value):
    dd = TimeLineStat[TimeLineStat['Имя команды'] == value]
    return px.line(dd, x='Дата', y='Число использований')


if __name__ == '__main__':
    arelocal = True
    if arelocal:
        app.run_server(debug=True)
    else:
        app.run_server(debug=False, host='0.0.0.0')
