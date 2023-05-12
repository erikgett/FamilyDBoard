from dash import Dash, Input, Output, State, dcc, html, no_update, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from GetStaticticDF import family_history_table, family_news_table, family_table

FamilyHistoryTable = family_news_table(family_history_table(), family_table())
FamilyHistoryTable.sort_values(by='Дата', ascending=False, inplace=True)

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)

df = FamilyHistoryTable
df['id'] = df['Имя семейства']

app.layout = dbc.Container([
    dbc.Label('Click a cell in the table:'),
    dash_table.DataTable(
        df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns[:-2]],
        row_selectable='single',
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
        id='tbl'),
    dbc.Alert(id='tbl_out'),
    dbc.Alert(id='tbl_out2'),
])


@app.callback(
    (
            Output('tbl_out', 'children'),
            Output('tbl', 'selected_rows'),
    ), Input('tbl', 'active_cell'),
    prevent_initial_call=True)
def update_graphs(active_cell):
    return (
        str(active_cell),
        [active_cell['row']],
    ) if active_cell else (str(active_cell), no_update)


@app.callback(
    (
            Output('tbl_out2', 'children'),
            Output('tbl', 'style_data_conditional'),
            Output('tbl', 'active_cell'),
            Output('tbl', 'selected_cells')
    ),
    Input('tbl', 'derived_viewport_selected_row_ids'),
    State('tbl', 'derived_viewport_selected_rows'),
    State('tbl', 'active_cell'),
    State('tbl', 'selected_cells'),
    prevent_initial_call=True)
def update_graphs2(selected_row_ids, selected_rows, active_cell, selected_cells):
    if selected_row_ids:
        if active_cell:
            active_cell['row'] = selected_rows[0]
        else:
            active_cell = no_update
        return (
            str(f'{selected_row_ids} {selected_rows} {active_cell} {selected_cells}'),
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
        return "Click the table", [], no_update, []


if __name__ == '__main__':
    app.run_server(debug=True)