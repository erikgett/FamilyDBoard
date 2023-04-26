import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dash_table
from dash import dcc, callback, Output, Input
from dash import html
from datetime import datetime as dt

from GetStaticticDF import family_history_table, family_news_table

FamilyHistoryTable = family_news_table(family_history_table())

FamiliesNewsPage = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])

FamiliesNewsPage.layout = html.Div([
    html.Div(
        children=[
            html.P(children="🏢", className="header-emoji"),
            html.H1(children="Менеджер семейств", className="header-title"),
            html.P(
                children="В данном разделе предоставлена информация по актуальным\n"
                         "обновлениям семейств в репозитории семейств\n",
                className="header-description",
            )
        ],
        className="header",
    ),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3(children='Промежуток времени для истории',
                        style={'font-size': '14px', 'padding': '16px 20px 0 0', 'color': '#000000', 'font-weight': 'bold'}),
                dcc.DatePickerRange(
                    id='my-date-picker-range',  # ID to be used for callback
                    calendar_orientation='horizontal',  # vertical or horizontal
                    day_size=39,  # size of calendar image. Default is 39
                    end_date_placeholder_text="Return",  # text that appears when no end date chosen
                    with_portal=False,  # if True calendar will open in a full screen overlay portal
                    first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
                    reopen_calendar_on_clear=True,
                    is_RTL=False,  # True or False for direction of calendar
                    clearable=True,  # whether or not the user can clear the dropdown
                    number_of_months_shown=1,  # number of months shown when calendar is open
                    min_date_allowed=dt(2022, 1, 1),  # minimum date allowed on the DatePickerRange component
                    max_date_allowed=dt(2025, 1, 1),  # maximum date allowed on the DatePickerRange component
                    initial_visible_month=dt(2023, 4, 25),
                    # the month initially presented when the user opens the calendar
                    start_date=dt(2023, 4, 23).date(),
                    end_date=dt(2020, 4, 26).date(),
                    display_format='MMM Do, YY',  # how selected dates are displayed in the DatePickerRange component.
                    month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
                    minimum_nights=1,  # minimum number of days between start and end date

                    persistence=True,
                    persisted_props=['start_date'],
                    persistence_type='session',  # session, local, or memory. Default is 'local'

                    updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
                )
            ]),
            dbc.Col([
                html.H3(children='Отметьте необходимый для вас раздел',
                        style={'font-size': '14px', 'padding': '16px 20px 0 0', 'color': '#000000', 'font-weight': 'bold'}),
                dcc.Dropdown(['ОВ', 'ВК'], 'ВК')
            ]),
            dbc.Col([
                html.H3(children='Что отобразить (новые семейства/обновления/всё)',
                        style={'font-size': '14px', 'padding': '16px 20px 0 0', 'color': '#000000', 'font-weight': 'bold'}),
                dcc.Dropdown(['Новые семейства', 'Свежие обновления', 'Все семейства'], 'Все семейства')
            ]),
        ]),
    ]),

    html.H3(children='⠀', style={'textAlign': 'center'}),
    html.H3(children='Таблица внесенных изменений в репозиторий семейств', style={'textAlign': 'center'}),
    html.H3(children='⠀', style={'textAlign': 'center'}),

    dash_table.DataTable(FamilyHistoryTable.to_dict('records'),
                         [{"name": i, "id": i} for i in FamilyHistoryTable.columns]),
])


@callback(Output('graph-content', 'figure'), Input('dropdown-selection', 'value'))
def update_graph(value):

    return dash_table.DataTable(FamilyHistoryTable.head(5).to_dict('records'),
                                [{"name": i, "id": i} for i in FamilyHistoryTable.columns])

if __name__ == '__main__':
    arelocal = True
    if arelocal:
        FamiliesNewsPage.run_server(debug=True)
    else:
        FamiliesNewsPage.run_server(debug=False, host='0.0.0.0')
