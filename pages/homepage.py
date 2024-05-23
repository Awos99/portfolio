import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
import pandas as pd


profile_img = html.Img(src="../static/profile.jpg", 
                        className="img-fluid rounded-4",
                        style={"margin": "10%"})


def interest_card(src, title, text):
    return dbc.Card(
        [
            dbc.CardImg(src=src, 
                        top=True,
                        style={"maxHeight": "60px", "objectFit": "scale-down"}),
            dbc.CardBody(
                [
                    html.H4(title, className="card-title"),
                    html.P(
                        text,
                        className="card-text",
                    ),
                ]
            ),
        ],
        className="card mb-3 text-center align-items-center",
        style={"max-width": "20rem",
                "margin": "10px",
                "backgroundColor": "transparent",
                "border": "none"},
    )

df_interests = pd.read_excel("static/interests.xlsx")


def interests_matrix(df_interests):
    num_interests = len(df_interests)
    num_cols = 3
    num_rows = num_interests // num_cols
    matrix = []
    if num_interests % num_cols != 0:
        num_rows += 1
    for row in range(num_rows):
        row_elements = []
        for col in range(num_cols):
            index = row * num_cols + col
            if index < num_interests:
                row_elements.append(dbc.Col(interest_card(df_interests.iloc[index]["src"], df_interests.iloc[index]["title"], df_interests.iloc[index]["text"]),
                                            className="d-flex justify-content-center"))
        matrix.append(dbc.Row(row_elements))
    

    return matrix


jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Areas of Interest", className="display-4 text-center"),
            html.P(
                "Take a look at things I love working on.",
                className="lead text-center",
            ),
            html.Hr(className="my-2"),
        ] + interests_matrix(df_interests),
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-body-secondary rounded-3 my-3",
)

container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3("I am", className="display-6"),
                                html.H1("Amos Wolf", className="display-3"),
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
                            ],
                        ),
                        html.Button("My Projects", className="btn btn-primary btn-lg"),
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
        ),
        dbc.Row(
            jumbotron
        ),
    ],
    className="mt-5",
)

def get_homepage():
    return container