import dash
from dash import dcc, html, Input, Output
from pages.statistics import layout
import dash_bootstrap_components as dbc
from pages.main import layout as main_layout
from dash_bootstrap_components._components.Container import Container
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
# app = dash.Dash(__name__, suppress_callback_exceptions=True)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Avtohalokatlar"
application = app.server

buttons = dbc.Row(
    [
        dbc.Col([
            dbc.Button("Regular", color="dark", className="me-1"),
            dbc.Button("Active", color="dark", active=True, className="me-1"),
            dbc.Button("Disabled", color="dark", disabled=True),
        ])
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar (
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Avtohalokatlar", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                buttons,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    expand='lg',
)

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = True),
    html.Div(id = 'page_content')]
)

@app.callback(
    Output('page_content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/page-1':
        return layout
    else:
        return main_layout

if __name__ == '__main__':
    app.run_server()