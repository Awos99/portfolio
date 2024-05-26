import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
from dash_bootstrap_components._components.Container import Container
import pandas as pd
import asyncio
from calculations.readmes_repos import get_repos_5h, get_number_followers
import ast
from app import app
from threading import Thread
from components.github_graphs import heatmap_github, languages_github
import requests




# Run the task using the asyncio event loop
def run_asyncio_task(task):
    asyncio.run(task)

thread = Thread(target=run_asyncio_task, args=(get_repos_5h(),))
thread.daemon = True
thread.start()

df_repos = pd.read_csv("static/repos.csv")
df_repos['topics'] = df_repos['topics'].apply(ast.literal_eval)
df_repos['commits'] = df_repos['commits'].apply(ast.literal_eval)
df_repos['owner'] = df_repos['owner'].apply(ast.literal_eval)
image_profile_url=df_repos['owner'][0]['avatar_url']
profile_name_github = df_repos['owner'][0]['login']
url_github = df_repos['owner'][0]['html_url']

number_followers = get_number_followers(df_repos['owner'][0]['followers_url'])

image_profile = html.Img(src=image_profile_url, 
                        className="img-fluid rounded-circle border border-1 ",
                        style={'background-color': 'white',
                               'height': '300px',})
# add graphs to container
graphs = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                
                                dbc.Col(
                                    [
                                        dcc.Graph(figure=heatmap_github(df_repos),
                                                  style={'height': '140px',
                                                         'width': '455px'},
                                                         ),
                                    ],
                                    width='auto'
                                    
                                    
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(figure=languages_github(df_repos),
                                                  style={'height': '135px',
                                                         'width':'350px'},
                                                         ),
                                    ],
                                    width='auto'
                                    
                                ),
                            ],
                            className="rounded border p-1 border-1 ",
                            style={'background-color': 'white'}
                            
                        ),
                    ],
                    width='auto',
                ),
            ],
            align="center",
            className="mt-5 align-items-center justify-content-center",
        ),
    ],
    className="mt-5 align-items-center justify-content-center",
    
)

def repository_card(src, title, text, readme=None, url_github=None):
    flag_img=0
    if 'GIF' in readme:
        src = f'https://raw.githubusercontent.com/Awos99/{title}/main/static/demo.gif?token=GHSAT0AAAAAACQPEY4CJW2MT67CGPPLYAFYZSTO5PA'
        flag_img=1
        readme=readme.replace('![Demo GIF](/static/demo.gif)', '')
        
    
    card_img=dbc.CardImg(src=src, 
                        top=True,
                        )
    
    if flag_img==1:
        inside_modal=[dcc.Markdown(readme), card_img]
    else:
        inside_modal=[dcc.Markdown(readme)]
    
    modal = html.Div(
        [
            dbc.Button("More...", id="open" + title.replace('.', '').replace('{', ''), n_clicks=0),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle(title)),
                    dbc.ModalBody(inside_modal),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close"+title.replace('.', '').replace('{', ''), className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="modal" + title.replace('.', '').replace('{', ''),
                size="lg",
                is_open=False,
                
                
            ),
        ],
        style={'text-align': 'right'}
    )


    @app.callback(
        Output("modal"+title.replace('.', '').replace('{', ''), "is_open"),
        [Input("open" + title.replace('.', '').replace('{', ''), "n_clicks"), Input("close" + title.replace('.', '').replace('{', ''), "n_clicks")],
        [State("modal"+title.replace('.', '').replace('{', ''), "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open
    
    card_img=dbc.CardImg(src=src, 
                        top=True,
                        style={"maxHeight": "100px", "objectFit": "scale-down"})
    
    return dbc.Card(
        [   
            html.A([
                card_img,
                        
            ],
            
            href=url_github,
            target="_blank"),
            
            dbc.CardBody(
                [
                    html.H4(readme.split('\n')[0].replace('#', '').strip(), 
                            className="card-title",
                            style={"fontSize": "1.1rem",
                                   'height': '55px',}),
                    html.P(
                        text,
                        className="card-text",
                        style={"fontSize": "0.8rem",
                               'height': '150px',}
                    ),
                    modal,
                ]
            ),
        ],
        className="card my-3",
        style={"width": "18rem",
                "backgroundColor": "transparent"},
    )

def repositories_matrix(df_interests):
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
                row_elements.append(dbc.Col(repository_card('static/github_logo.png', df_interests.iloc[index]["name"], df_interests.iloc[index]["description"], df_interests.iloc[index]["readme"], df_interests.iloc[index]["html_url"]),
                                            className="d-flex justify-content-center"))
        matrix.append(dbc.Row(row_elements))
    

    return matrix

github_img_graphs = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        image_profile,
                        html.H3(profile_name_github),
                        html.A("Github Profile", href=url_github),
                        html.H5(f"Followers: {number_followers}",
                                className="lead"),
                        
                    ],
                    width=3,
                ),
                dbc.Col([graphs]+
                    
                        repositories_matrix(df_repos),
                
                    width=9,
                    align='center',
                    className='justify-content-center align-items-center',
                ),
            ],
            
        ),
    ],
)

jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Github Repository", className="display-4"),
            html.P(
                "Take a look at things I have been working on.",
                className="lead",
            ),
            html.Hr(className="my-2"),
        ] + [github_img_graphs],
        fluid=True,
        className="py-3",
    ),
    className="p-3 rounded-3 my-3",
    style={'background-color': 'white'}
)


container = dbc.Container(
    [
        html.Div(
            [
            
        ],
        style={'height': '10px'}
        ),
        jumbotron,
    ],
    className="mt-5",
)




def get_portfolio_page():
    return container


if __name__ == '__main__':
    app.run(debug=True)