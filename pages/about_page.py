import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
import pandas as pd

friends_img = html.Img(src="../static/friends.jpg",
                        className="img-fluid rounded-4",
                        style={"maxHeight": "500px", 
                               "objectFit": "scale-down",
                               "margin": "10%"})

download_cv = dbc.Button(
            "Download CV",
            href="../static/CV.pdf",
            download="Amos Wolf CV.pdf",
            external_link=True,
            color="primary",
            className="ms-auto btn-lg",
        )


df_funfacts = pd.read_excel("static/fun_facts.xlsx")
fun_facts = [{
    "key": str(i),
    "src": "../static/funfacts.png",
    "header": row["header"],
    "caption": row["caption"],
} for i, row in df_funfacts.iterrows()]

carousel = dbc.Carousel(
    items=fun_facts,
    variant="dark",
    controls=False,
    indicators=False,
    interval=4000,
    ride="carousel",
)

df_experiences = pd.read_excel("static/experiences.xlsx")


experiences = html.Div([
    html.H1("Professional Experiences", className="display-4 text-center"),
    ] +
    [
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H5(str(pd.to_datetime(row['start']).strftime('%B %Y')) + ' to ' + str(pd.to_datetime(row['end']).strftime('%B %Y'))),
                    html.H2(row['role']),
                    html.H1(row['company'], className="lead"),
                ],
                width=6,
            ),
            dbc.Col(
                html.P(row['description']),
                width=6,
            ),
        ],
        align="center",
        justify="center",
        className="my-5",
    )
    for i, row in df_experiences.iterrows()
],

)

df_education = pd.read_excel("static/education.xlsx")

education = html.Div(
    [
    dbc.Row(
        [
            dbc.Col(
                html.H1("Education", className="display-4"),
            ),
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H5(str(pd.to_datetime(row['start']).strftime('%B %Y')) + ' to ' + str(pd.to_datetime(row['end']).strftime('%B %Y'))),
                                    html.H2(row['name']),
                                    html.H1(row['istitution'], className="lead"),
                                ],
                            ),
                            dbc.Col(
                                [
                                    html.P(row['comments']),
                                ],
                            ),
                        ],
                        
                        
                        className="my-5",
                        align='center',
                    )
                    for i, row in df_education.iterrows()
                ],
                width=9,
                
            ),
        ],
        align="center",
        justify="center",
        className="my-2",
    )
    
],

)

def language_card(language, value, level):
    return html.Div(
        [
            html.H1(language),
            dbc.Progress(label=level, 
                            value=value,
                            id=f"language-{language}",
                            style={"height": "30px", "fontSize": "1rem"},
                            color="success"),
            dbc.Tooltip(f"{level} in {language}",
                        target=f"language-{language}",
                        placement="bottom",
                        style={"fontSize": "1rem"}),
        ],
        className="text-center",
        style={"width": "300px"},
    )

def language_matrix(df_languages):
    num_interests = len(df_languages)
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
                row_elements.append(dbc.Col(language_card(df_languages.iloc[index]["language"], df_languages.iloc[index]["value"], df_languages.iloc[index]["level"]),
                                            className="d-flex justify-content-center"))
        matrix.append(dbc.Row(row_elements,
                                className="my-5"))
    return matrix

languages = html.Div([
    html.H1("Languages", className="display-4 text-center"),
    ] +
    language_matrix(pd.read_excel("static/languages.xlsx")))


container = dbc.Container(
    [
        dbc.Row(
            [
                
                dbc.Col(friends_img,
                    width=6,
                    className="d-flex align-items-center justify-content-center",
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3("I love creating meaningful impact, and I strive to produce work that I can take pride in", className="display-6"),
                                #html.H1("Amos Wolf", className="display-3"),
                                #html.P("Data Scientist and Consultant", className="lead"),
                                html.Blockquote(
                                    [
                                        html.P(
                                            "Throughout my academic and professional journey, I've actively sought out opportunities to collaborate with outstanding individuals and position myself in environments leading to growth and excellence.",
                                            className="mb-0",
                                        ),
                                    ],
                                    className="blockquote",
                                ),
                            ],
                        ),
                        download_cv,
                    ],
                    width=6,
                ),
            ],
            align="center",
            justify="center",
        ),
        carousel,
        html.Hr(className="my-2"),
        experiences,
        html.Hr(className="my-2"),
        education,
        html.Hr(className="my-2"),
        languages,
    ],
    className="mt-5",
)


def get_about_page():
    return container