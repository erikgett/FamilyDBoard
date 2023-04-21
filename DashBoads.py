import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
import sqlite3
import plotly.express as px

con = sqlite3.connect(r"C:\Users\erik_\Documents\МОИ_ДОКУМЕНТЫ\FM_statistics.db")

df = pd.read_sql_query("SELECT * FROM UserAction", con)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-item'),
                width={'size': 6}),
        dbc.Col(dcc.Graph(id='graph-type'),
                width={'size': 6})
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-project'),
                width={'size': 6}),
        dbc.Col(dcc.Graph(id='graph-command'),
                width={'size': 6})
    ])
])



def update_graphs(selected_username):
    filtered_df = df[df['UserName'] == selected_username]

    item_counts = filtered_df['ItemName'].value_counts()
    item_fig = px.bar(x=item_counts.index, y=item_counts.values, title='Item Count')

    type_counts = filtered_df['TypeName'].value_counts()
    type_fig = px.pie(names=type_counts.index, values=type_counts.values, title='Type Distribution')

    project_counts = filtered_df['Project'].value_counts()
    project_fig = px.pie(names=project_counts.index, values=project_counts.values, title='Project Distribution')

    command_counts = filtered_df['CommandName'].value_counts()
    command_fig = px.bar(x=command_counts.index, y=command_counts.values, title='Command Count')

    return item_fig, type_fig, project_fig, command_fig

if __name__ == '__main__':
    print(df)
    app.run_server(debug=True)
