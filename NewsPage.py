import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dash_table
from dash import dcc, callback, Output, Input
from dash import html, no_update, State
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
from GetStaticticDF import family_history_table, family_news_table, family_table

FamilyHistoryTable = family_news_table(family_history_table(), family_table())
FamilyHistoryTable.sort_values(by='Дата', ascending=False, inplace=True)

# FamiliesNewsPage = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI], requests_pathname_prefix='/FamiliesNewsPage/')
FamiliesNewsPage = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])

FamilyHistoryTable['id'] = FamilyHistoryTable['Имя семейства']


def list_with_unique_coloms(FamilyHistoryTable):
    not_unique = list(FamilyHistoryTable['Раздел'].unique())
    not_unique.append('Все разделы')
    out_list = []
    for i in not_unique:
        items = i.split(',')
        for j in items:
            out_list.append(j)

    return list(set(out_list))


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
                    max_date_allowed=dt(2030, 1, 1), initial_visible_month=dt(2023, 4, 25),
                    start_date=dt((dt.now() - timedelta(days=10)).year, (dt.now() - timedelta(days=10)).month,
                                  (dt.now() - timedelta(days=10)).day).date(),
                    end_date=dt(dt.now().year, dt.now().month, dt.now().day).date(),
                    display_format='MMM Do, YY', month_format='MMMM, YYYY',
                    minimum_nights=1, persistence=True, persisted_props=['start_date'],
                    persistence_type='session', updatemode='singledate'
                )
            ]),
            dbc.Col([html.H3(children=' ')]),
            dbc.Col([
                html.H3(children='Отметьте необходимый для вас раздел',
                        style={'font-size': '14px', 'padding': '16px 20px 0 0',
                               'color': '#000000', 'font-weight': 'bold'}),
                dcc.Dropdown(list_with_unique_coloms(FamilyHistoryTable),
                             'Все разделы', id='set_chapter')
            ]),
        ]),
    ]),

    html.H3(children='⠀', style={'textAlign': 'center'}),
    html.H3(children='Таблица внесенных изменений в репозиторий семейств', style={'textAlign': 'center'}),
    html.H3(children='⠀', style={'textAlign': 'center'}),

    dash_table.DataTable(
        data=FamilyHistoryTable.to_dict('records'),
        columns=[{"name": i, "id": i} for i in FamilyHistoryTable.columns[:-2]],
        page_size=20,
        cell_selectable=True,
        style_data_conditional=[
            {
                "if": {
                    "state": "active"  # 'active' | 'selected'
                },
                "backgroundColor": "rgba(0, 116, 217, 0.3)",
                "border": "1px solid rgb(0, 116, 217)",
            },
            {
                "if": {
                    "state": "selected"  # 'active' | 'selected'
                },
                "backgroundColor": "rgba(0, 116, 217, 0.3)",
                "border": "1px solid rgb(0, 116, 217)",
            }

        ],
        id='datatable-interactivity'),

    html.H3(children='⠀', style={'textAlign': 'center'}),
    dbc.Alert(id='tbl_out', style={'margin': '0px 20px 0px 20px'}, color="light"),
    html.H3(children='⠀', style={'textAlign': 'center'}),
    html.H3(children='Таблица для конкретного семейства', style={'textAlign': 'center'}),
    html.H3(children='⠀', style={'textAlign': 'center'}),
    dash_table.DataTable(
        data=FamilyHistoryTable.to_dict('records'),
        page_size=20,
        id='selectedItem'),
])


@FamiliesNewsPage.callback((Output('tbl_out', 'children'), Output('datatable-interactivity', 'selected_rows'),),
                           Input('datatable-interactivity', 'active_cell'),
                           prevent_initial_call=True)
def update_graphs(active_cell):
    if active_cell:
        return str(active_cell) + str([active_cell['row']]) + str([active_cell['row_id']]), [active_cell['row']]
    else:
        return "Нажмите на семейство, чтобы увидеть подробную историю о семействе", []


def string_to_pd_date(date):
    return pd.to_datetime(pd.Series(date))[0]


# Фильтрация таблицы по календарю и разделам
@FamiliesNewsPage.callback(
    dash.dependencies.Output("datatable-interactivity", "data"),
    [
        dash.dependencies.Input("my-date-picker-range", "start_date"),
        dash.dependencies.Input("my-date-picker-range", "end_date"),
        dash.dependencies.Input("set_chapter", "value")])
def update_data(start_date, end_date, chapter):
    out_df = FamilyHistoryTable[pd.to_datetime(FamilyHistoryTable['Дата']) >= string_to_pd_date(start_date)]
    out_dff = out_df[pd.to_datetime(out_df['Дата']) <= string_to_pd_date(end_date)]
    if chapter != 'Все разделы':
        out_dff = out_dff[out_dff['Раздел'] == chapter]

    date = out_dff.to_dict("records")
    return date


# Выделение необходимых строк
@FamiliesNewsPage.callback(
    (
        Output('datatable-interactivity', 'style_data_conditional'),
        Output('datatable-interactivity', 'active_cell'),
        Output('datatable-interactivity', 'selected_cells')
    ),
    Input('datatable-interactivity', 'derived_viewport_selected_row_ids'),
    State('datatable-interactivity', 'derived_viewport_selected_rows'),
    State('datatable-interactivity', 'active_cell'),
    prevent_initial_call=True)
def update_graphs2(selected_row_ids, selected_rows, active_cell):
    if selected_row_ids:
        if active_cell:
            active_cell['row'] = selected_rows[0]
        else:
            active_cell = no_update
        return (
            [
                {
                    "if": {
                        "filter_query": "{{id}} = '{}'".format(i)
                    },
                    "backgroundColor": "rgba(0, 116, 217, 0.3)",
                    "border": "1px solid rgb(0, 116, 217)",
                } for i in selected_row_ids
            ] + [
                {
                    "if": {
                        "state": "active"  # 'active' | 'selected'
                    },
                    "backgroundColor": "rgba(0, 116, 217, 0.3)",
                    "border": "1px solid rgb(0, 116, 217)",
                }
            ],
            active_cell,
            []
        )
    else:
        return [], no_update, []


# Фильтрация таблицы по выбранному семейству в другой таблице
@FamiliesNewsPage.callback(
    dash.dependencies.Output("selectedItem", "data"),
    [
        Input('datatable-interactivity', 'active_cell'),
    ])

def updateFamilyItem( active_cell):
    try:
        familyName = active_cell['row_id']
        if familyName == None:
            familyName =''
    except: familyName =''

    out_df = FamilyHistoryTable[FamilyHistoryTable['Имя семейства'] == familyName]
    date = out_df.to_dict("records")
    return date

if __name__ == '__main__':
    FamiliesNewsPage.run_server(debug=False)


