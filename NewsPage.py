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
                html.H3(children='Промежуток времени истории обновлений',
                        style={'font-size': '14px', 'padding': '16px 20px 0 0',
                               'color': '#000000', 'font-weight': 'bold'}),
                dcc.DatePickerRange(
                    id='my-date-picker-range', calendar_orientation='horizontal',
                    day_size=39, end_date_placeholder_text="Return",
                    with_portal=False, first_day_of_week=1,
                    reopen_calendar_on_clear=True, is_RTL=False,
                    clearable=True, number_of_months_shown=1, min_date_allowed=dt(2022, 1, 1),
                    max_date_allowed=dt(2025, 1, 1), initial_visible_month=dt(2023, 4, 25),
                    start_date=dt(2023, 4, 23).date(), end_date=dt(2023, 4, 26).date(),
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
                dcc.Dropdown(['Новые семейства', 'Свежие обновления', 'Все семейства'], 'Все семейства',
                             id='update_new_load')
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


def string_to_pd_date(date):
    return pd.to_datetime(pd.Series(date))[0]


@FamiliesNewsPage.callback(
    dash.dependencies.Output("datatable-interactivity", "data"),
    [
        dash.dependencies.Input("my-date-picker-range", "start_date"),
        dash.dependencies.Input("my-date-picker-range", "end_date"),
        dash.dependencies.Input("update_new_load", "value"),
    ],)
def update_data(start_date, end_date, value):
    # отсортировали по дате
    out_df = FamilyHistoryTable[pd.to_datetime(FamilyHistoryTable['Дата']) >= string_to_pd_date(start_date)]
    out_dff = out_df[pd.to_datetime(out_df['Дата']) <= string_to_pd_date(end_date)]
    # отсортировать по загружено новое обновление все
    if value =='Новые семейства':
        out_dff = out_dff[out_dff['Версия семейства'] == '1.0.0']
    elif value =='Свежие обновления':
        out_dff = out_dff[out_dff['Версия семейства'] != '1.0.0']

    date = out_dff.to_dict("records")
    return date


if __name__ == '__main__':
    FamiliesNewsPage.run_server(debug=True)
