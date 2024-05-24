from app import app
from components.header import get_header
from components.footer import get_footer
import dash_bootstrap_components as dbc
from pages.homepage import get_homepage
from pages.portfolio_page import get_portfolio_page
from dash import Dash, dcc, html, Input, Output, callback, State
import os
from pages.about_page import get_about_page

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    get_header(),
    html.Div([
        get_homepage(),
    ],
    id="page-content"),
    get_footer(),
],
)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return get_homepage()
    elif pathname == '/about':
        return get_about_page()
    elif pathname == '/portfolio':
        return get_portfolio_page()
    elif pathname == '/huck':
        return get_huck_page()
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )

if __name__ == '__main__':
    app.run(debug=True)