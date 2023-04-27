import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dash_table
from dash import dcc, callback, Output, Input
from dash import html
from datetime import datetime as dt
import pandas as pd
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
                        style={'font-size': '14px', 'padding': '16px 20px 0 0',
                               'color': '#000000', 'font-weight': 'bold'}),
                dcc.DatePickerRange(
                    id='my-date-picker-range', calendar_orientation='horizontal',
                    day_size=39, end_date_placeholder_text="Return",
                    with_portal=False, first_day_of_week=1,
                    reopen_calendar_on_clear=True, is_RTL=False,
                    clearable=True, number_of_months_shown=1, min_date_allowed=dt(2022, 1, 1),
                    max_date_allowed=dt(2025, 1, 1), initial_visible_month=dt(2023, 4, 25),
                    start_date=dt(2023, 4, 23).date(), end_date=dt(2020, 4, 26).date(),
                    display_format='MMM Do, YY', month_format='MMMM, YYYY',
                    minimum_nights=1, persistence=True, persisted_props=['start_date'],
                    persistence_type='session', updatemode='singledate'
                )
            ]),
            dbc.Col([
                html.H3(children='Отметьте необходимый для вас раздел',
                        style={'font-size': '14px', 'padding': '16px 20px 0 0',
                               'color': '#000000', 'font-weight': 'bold'}),
                dcc.Dropdown(['ОВ', 'ВК'], 'ВК')
            ]),
            dbc.Col([
                html.H3(children='Что отобразить (новые семейства/обновления/всё)',
                        style={'font-size': '14px', 'padding': '16px 20px 0 0',
                               'color': '#000000', 'font-weight': 'bold'}),
                dcc.Dropdown(['Новые семейства', 'Свежие обновления', 'Все семейства'], 'Все семейства')
            ]),
        ]),
    ]),

    html.H3(children='⠀', style={'textAlign': 'center'}),
    html.H3(children='Таблица внесенных изменений в репозиторий семейств', style={'textAlign': 'center'}),
    html.H3(children='⠀', style={'textAlign': 'center'}),

    dash_table.DataTable(data=FamilyHistoryTable.to_dict('records'),
                         columns=[{"name": i, "id": i} for i in FamilyHistoryTable.columns],
                         page_size=20, id='datatable-interactivity'),
])


@FamiliesNewsPage.callback(
    dash.dependencies.Output("datatable-interactivity", "data"),
    [
        dash.dependencies.Input("my-date-picker-range", "start_date"),
        dash.dependencies.Input("my-date-picker-range", "end_date"),
    ],
)
def update_data(start_date, end_date):
    date = FamilyHistoryTable.to_dict("records")
    if start_date and end_date:
        mask = (FamilyHistoryTable["Дата"] >= start_date) \
               & (FamilyHistoryTable["Дата"] <= end_date)
        data = FamilyHistoryTable.loc[mask].to_dict("records")
    return date


if __name__ == '__main__':
    if True:
        FamiliesNewsPage.run_server(debug=True)
    else:
        FamiliesNewsPage.run_server(debug=False, host='0.0.0.0')
