import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
from dash_bootstrap_components._components.Container import Container
import pandas as pd
import asyncio
from calculations.readmes_repos import get_repos_5h
import ast
from app import app
from threading import Thread
from components.github_graphs import heatmap_github, languages_github

# Run the task using the asyncio event loop
def run_asyncio_task(task):
    asyncio.run(task)

thread = Thread(target=run_asyncio_task, args=(get_repos_5h(),))
thread.daemon = True
thread.start()

df_repos = pd.read_csv("static/repos.csv")
df_repos['topics'] = df_repos['topics'].apply(ast.literal_eval)
df_repos['commits'] = df_repos['commits'].apply(ast.literal_eval)

# add graphs to container
graphs = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("GitHub Repositories", className="display-4"),
                    ],
                    width=12,
                ),
            ],
            align="center",

        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(figure=heatmap_github(df_repos),
                                                  style={'height': '115px',
                                                         'width': '450px'},
                                                         className="rounded border my-2"), # fix this
                                    ],
                                    width=6,
                                    
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(figure=languages_github(df_repos),
                                                  style={'height': '280px',
                                                         'width':'600px'}),
                                    ],
                                    width=3,
                                ),
                            ],
                        ),
                    ],
                    width=12,
                ),
            ],
            align="center",
        ),
    ],
    className="mt-5",
)


container = dbc.Container(
    [
        graphs,
    ],
    className="mt-5",
)




def get_portfolio_page():
    return container


if __name__ == '__main__':
    app.run(debug=True)