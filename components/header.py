import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
from app import app

#PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto",
    align="center",
)

download_cv = dbc.Button(
            "Download CV",
            href="../static/CV.pdf",
            download="Amos Wolf CV.pdf",
            external_link=True,
            color="primary",
            className="ms-auto",
        )

nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("About", href="/about")),
        dbc.NavItem(dbc.NavLink("Portfolio", href="/portfolio")),
        dbc.NavItem(dbc.NavLink("Contact", href="/contact")),
    ],
    justified=True,
    navbar=True
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            #html.A(
                # Use row and col to control vertical alignment of logo / brand
            #    dbc.Row(
            #        [
            #            dbc.Col(html.Img(src="../static/oie_jpg.ico", height="30px")),
            #            dbc.Col(dbc.NavbarBrand("Amos Wolf")),
            #        ],
            #        align="center",
            #        className="g-0",
            #    ),
            #    href="#",
                #style={"textDecoration": "none"},
            #),
            dbc.NavbarBrand("Amos Wolf"),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                [nav, 
                download_cv
                ],
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    fixed="top",
    style={
        "backgroundColor": 'rgb(245, 244, 242)',
        'border': '1px solid rgb(215, 207, 193)',
    }
    #color="dark",
    #dark=True,
)


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

def get_header():
    return navbar


