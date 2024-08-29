import dash
from dash import dcc, ctx, dash_table
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from dataclasses import dataclass
import portal.ui_shared as ui_shared
import pandas as pd

# Assume images are numpy arrays
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
# Create a Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc_css], suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Add a Plotly graph and a slider to the application layout
recon_catalog_layout = dbc.Container(
    [html.Div([
        ui_shared.navbar,
        dbc.Row(
            [
                dash_table.DataTable(
                    id='recon-table',
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    page_action="native",
                    page_current= 0,
                    page_size= 20,
                )
            ],
            style={'width': '100%', 'overflow-x': 'auto'}
        )
    ],
    )
    ],
    className='dbc', 
    fluid=True
)


create_recon_layout = dbc.Container(
    [html.Div([
        ui_shared.navbar,
        dbc.Row(
                [
                    dbc.Accordion(
                        [
                        dbc.AccordionItem(
                            [
                                html.P("This is the content of the first section"),
                                dbc.Button("Click here"),
                            ],
                            title="Recon Parameters",
                        ),
                        dbc.AccordionItem(
                            [
                                html.P("This is the content of the second section"),
                                dbc.Button("Don't click me!", color="danger"),
                            ],
                            title="Calibration",
                        ),
                        dbc.AccordionItem(
                            "This is the content of the third section",
                            title="Mask",
                        ),
                        dbc.AccordionItem(
                            "This is the content of the third section",
                            title="Motor Path",
                        ),
                        dbc.AccordionItem(
                            "This is the content of the third section",
                            title="Detector",
                        ),
                        dbc.AccordionItem(
                            "This is the content of the third section",
                            title="Algorithm Parameters",
                        ),
                        ],
                        always_open=True
                    ),
                ],
                style={'width': '100%', 'overflow-x': 'auto'}
        )
    ],
    )
    ],
    className='dbc', 
    fluid=True
)




"""
================
Multi-page Callbacks
================
"""

# Update the index
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return recon_catalog_layout
    elif pathname == '/recons':
        return recon_catalog_layout
    elif pathname == '/new-recon':
        return create_recon_layout

    #else:
    #    return index_page
    # You could also return a 404 "URL not found" page here


# Run the application
if __name__ == '__main__':
    app.run_server(debug=True, port=2051, host='0.0.0.0')