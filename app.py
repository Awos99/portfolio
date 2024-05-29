from dash import Dash

app = Dash(__name__, external_stylesheets= ["/assets/bootstrap.css"], suppress_callback_exceptions=True)
server = app.server