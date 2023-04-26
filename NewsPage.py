import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dash_table
from dash import dcc, callback, Output, Input
from dash import html

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
    dash_table.DataTable(FamilyHistoryTable.to_dict('records'), [{"name": i, "id": i} for i in FamilyHistoryTable.columns]),
])

if __name__ == '__main__':
    arelocal = True
    if arelocal:
        FamiliesNewsPage.run_server(debug=True)
    else:
        FamiliesNewsPage.run_server(debug=False, host='0.0.0.0')
