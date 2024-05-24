import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
from app import app

footer = dbc.Container(
    [
        html.Hr(className="my-2"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5("Contact"),
                        html.P("Email: contact@amoswolf.com", 
                               className="lead",
                               style={"font-size": "1rem"}),
                        html.P("Phone: +39 1234567890", 
                               className="lead",
                               style={"font-size": "1rem"}),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.H5("Social"),
                        html.P("LinkedIn: Amos Wolf", 
                               className="lead",
                               style={"font-size": "1rem"}),
                        html.P("GitHub: Awos99", 
                               className="lead",
                               style={"font-size": "1rem"}),
                    ],
                    width=6,
                ),
            ],
        ),
    ],
    className="p-5",
)

def get_footer():
    return footer