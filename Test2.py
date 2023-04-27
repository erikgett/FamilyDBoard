import pandas as pd
import dash
import dash_table
from dash.dependencies import Input, Output
from datetime import datetime as dt
import dash_core_components as dcc
import dash_html_components as html

df = pd.read_csv("Test_Time_Series.csv")
df["Date"] = pd.to_datetime(df.Date, errors="coerce")
df.index = df["Date"]

app = dash.Dash()

app.layout = html.Div(
    [
        dcc.DatePickerRange(
            id="my-date-picker-range",
            min_date_allowed=dt(2019, 1, 1),
            max_date_allowed=dt(2019, 1, 4),
            initial_visible_month=dt(2019, 1, 1),
            end_date=dt(2019, 1, 4),
        ),
        dash_table.DataTable(
            id="datatable-interactivity",
            columns=[
                {
                    "name": i,
                    "id": i,
                    "deletable": True,
                    "selectable": True,
                    "hideable": True,
                }
                if i == "iso_alpha3" or i == "year" or i == "id"
                else {"name": i, "id": i, "deletable": True, "selectable": True}
                for i in df.columns
            ],
            data=df.to_dict("records"),  # the contents of the table
            editable=True,  # allow editing of data inside all cells
            filter_action="native",  # allow filtering of data by user ('native') or not ('none')
            sort_action="native",  # enables data to be sorted per-column by user or not ('none')
            sort_mode="single",  # sort across 'multi' or 'single' columns
            column_selectable="multi",  # allow users to select 'multi' or 'single' columns
            row_selectable="multi",  # allow users to select 'multi' or 'single' rows
            row_deletable=True,  # choose if user can delete a row (True) or not (False)
            selected_columns=[],  # ids of columns that user selects
            selected_rows=[],  # indices of rows that user selects
            page_action="native",  # all data is passed to the table up-front or not ('none')
            page_current=0,  # page number that user is on
            page_size=6,  # number of rows visible per page
            style_cell={  # ensure adequate header width when text is shorter than cell's text
                "minWidth": 95,
                "maxWidth": 95,
                "width": 95,
            },
            style_cell_conditional=[  # align text columns to left. By default they are aligned to right
                {"if": {"column_id": c}, "textAlign": "left"}
                for c in ["country", "iso_alpha3"]
            ],
            style_data={  # overflow cells' content into multiple lines
                "whiteSpace": "normal",
                "height": "auto",
            },
        ),
    ]
)


def date_string_to_date(date_string):
    return pd.to_datetime(date_string, infer_datetime_format=True)


@app.callback(
    dash.dependencies.Output("datatable-interactivity", "data"),
    [
        dash.dependencies.Input("my-date-picker-range", "start_date"),
        dash.dependencies.Input("my-date-picker-range", "end_date"),
    ],
)
def update_data(start_date, end_date):
    data = df.to_dict("records")
    if start_date and end_date:
        mask = (date_string_to_date(df["Date"]) >= date_string_to_date(start_date)) & (
            date_string_to_date(df["Date"]) <= date_string_to_date(end_date)
        )
        data = df.loc[mask].to_dict("records")
    return data


if __name__ == "__main__":
    app.run_server(debug=True)