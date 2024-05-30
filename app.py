from dash import Dash

app = Dash(__name__, external_stylesheets= ["/assets/bootstrap.css"])
server = app.server