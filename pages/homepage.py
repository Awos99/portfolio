import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container


profile_img = html.Img(src="../static/profile.jpg", 
                        className="img-fluid rounded-4",
                        style={"margin": "10%"})

container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3("I am", className="text-body-secondary"),
                                html.H1("Amos Wolf"),
                                html.P("Data Scientist and Consultant", className="lead"),
                                html.Blockquote(
                                    [
                                        html.P(
                                            "Looking for my next opportunity to make a change. The digital way.",
                                            className="mb-0",
                                        ),
                                    ],
                                    className="blockquote",
                                ),

                                #html.Figcaption(
                                #    "Amos Wolf",
                                    
                                #    className="blockquote-footer",
                                #),
                                
                                
                            ],
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(profile_img,
                    width=6,
                    className="d-flex align-items-center justify-content-center",
                ),
            ],
            align="center",
            justify="center",
        )
    ]
)

def get_homepage():
    return container