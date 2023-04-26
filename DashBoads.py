import dash
import dash_bootstrap_components as dbc
from dash import dcc, callback, Output, Input
from dash import html
import pandas as pd
from dash import dash_table
from datetime import timedelta
import plotly.express as px

from GetStaticticDF import statistic_table, table_for_time_line_graf, family_history_table, table_for_bim_time_line_graf

statisticsPage = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI], requests_pathname_prefix="/statistics/")
FullTable = statistic_table()
TimeLineStat = table_for_time_line_graf(FullTable)
FamilyHistoryTable = family_history_table()
TimeLineBIMStat = table_for_bim_time_line_graf(FamilyHistoryTable)


statisticsPage.layout = html.Div([
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

    #   ПЕРВАЯ ЧАСТЬ РАЗДЕЛА
    html.H1(children="Часть первая - анализ активности использования менеджера семейств проектировщиками",
            className="header-title_black"),

    html.H3(children='График использования команд', style={'textAlign': 'center'}),

    html.H3(children='На данном графике можно увидеть сколько раз и какая команда была использована',
            className="header-description_black"),
    dcc.Graph(
        id='CommandClicked',
        figure={
            'data': [
                {'x': FullTable['Имя команды'], 'type': 'histogram'}
            ],
        }
    ),

    html.H3(children='Количество использованных команд пользователем', style={'textAlign': 'center'}),
    html.H3(children='На данном графике можно увидеть сколько раз '
                     'и какой пользователь пользовался командами данного плагина',
            className="header-description_black"),

    dcc.Graph(
        id='FamilyHistory1',
        figure={
            'data': [
                {'x': FullTable['UserName'], 'type': 'histogram'},

            ],
        }
    ),

    html.H3(children='Количество использованных команд по проектам', style={'textAlign': 'center'}),
    html.H3(children='На данном графике можно посмотреть на активность использования данного плагина в проектах',
            className="header-description_black"),
    dcc.Graph(
        id='FamilyHistory2',
        style={'margin-bottom': 10},
        figure={

            'data': [
                {'x': FullTable['Project'], 'type': 'histogram'}
            ],
            'layout': {'height': 500},
        },
    ),

    html.H3(children='⠀', style={'textAlign': 'center'}),
    html.H3(children='Динамика использования команд', style={'textAlign': 'center'}),
    html.H3(children='В таблице можно посмотреть в какой день и какими командами как часто пользовались',
            className="header-description_black"),
    html.H3(children='⠀', style={'textAlign': 'center'}),
    dash_table.DataTable(TimeLineStat.to_dict('records'), [{"name": i, "id": i} for i in TimeLineStat.columns]),

    html.H3(children='⠀', style={'textAlign': 'center'}),
    html.H3(children='График использования на временной линии', style={'textAlign': 'center'}),
    html.H3(children='На данном графике можно посмотреть на активность использования функций плагина в разрезе времени',
            className="header-description_black"),
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
                 id='dropdown-selection', style={'padding': '2px 20px 2px 20px'}), dcc.Graph(id='graph-content'),

    #   ВТОРАЯ ЧАСТЬ РАЗДЕЛА
    html.H1(children="Часть вторая - анализ активности работы BIM-специалистов",
            className="header-title_black"),

    html.H3(children='Число внесенных изменений от Bim-специалистов', style={'textAlign': 'center'}),
    html.H3(children='На данном графике можно посмотреть кто и когда вносил изменения в репозиторий',
            className="header-description_black"),
    html.H3(children='⠀', style={'textAlign': 'center'}),
    dcc.Graph(
        id='FamilyHistory',
        figure={
            'data': [
                {'x': FamilyHistoryTable['Creater'], 'type': 'histogram'}
            ],
        }
    ),

    html.H3(children='Число внесенных изменений от Bim-специалиста для конкретного семейства', style={'textAlign': 'center'}),
    html.H3(children='На данном графике можно посмотреть какие конкретного семейства и сколько раз корректировал специалист',
            className="header-description_black"),
    html.H3(children='⠀', style={'textAlign': 'center'}),
    dcc.Dropdown(FamilyHistoryTable['Creater'].unique(), FamilyHistoryTable['Creater'].unique()[0],
                 id='dropdown-selection2', style={'padding': '2px 20px 2px 20px'}), dcc.Graph(id='graph-content2'),

    html.H3(children='График активности Bim-специалиста по работе с семействами', style={'textAlign': 'center'}),
    html.H3(children='На данном графике можно посмотреть сколько изменений внес конкретный специалист в разрезе времени',
            className="header-description_black"),
    dcc.Dropdown(TimeLineBIMStat['Creater'].unique(), TimeLineBIMStat['Creater'].unique()[0],
                 id='dropdown-selection3', style={'padding': '2px 20px 2px 20px'}), dcc.Graph(id='graph-content3'),
])


@callback(Output('graph-content', 'figure'), Input('dropdown-selection', 'value'))
def update_graph(value):
    dd = TimeLineStat[TimeLineStat['Имя команды'] == value]
    return px.line(dd, x='Дата', y='Число использований')


@callback(Output('graph-content2', 'figure'), Input('dropdown-selection2', 'value'))
def update_graph2(value):
    dd = FamilyHistoryTable[FamilyHistoryTable['Creater'] == value]
    figure = {
        'data': [
            {'x': dd['Name'], 'type': 'histogram'}
        ],
    }
    return figure

@callback(Output('graph-content3', 'figure'), Input('dropdown-selection3', 'value'))
def update_graph3(value):
    dd = TimeLineBIMStat[TimeLineBIMStat['Creater'] == value]

    return px.line(dd, x='Дата', y='Число внесенных изменений')


if __name__ == '__main__':
    arelocal = True
    if arelocal:
        statisticsPage.run_server(debug=True)
    else:
        statisticsPage.run_server(debug=False, host='0.0.0.0')
