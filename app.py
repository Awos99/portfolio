from dash import Dash, dcc, html, Input, Output, callback, State
import os
from components import header
import dash_bootstrap_components as dbc
from pages.homepage import get_homepage



app = Dash(__name__, external_stylesheets= ["/assets/bootstrap.css"])

server = app.server



app.layout = html.Div([
    header.get_header(),
    get_homepage(),
])

header.get_callback(app)

if __name__ == '__main__':
    app.run(debug=True)