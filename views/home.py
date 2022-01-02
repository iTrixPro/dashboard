"""[Summary] :  home view."""

#============================================================================

# Created By   :  Marwan MEZROUI, Rayan SOBH, Etienne CHEVET
# Last Update  :  02/01/2022
# Version      :  1.0

#============================================================================
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from models.data import get_markers
import dash_leaflet as dl

NAVBAR_ICON = '../assets/img/logo.png'

def render():
    """Render the view.

    Returns:
        [Div]: view content
    """
    return html.Div(children=[navbar(), content()])

def searchbar():
    """Create a searchbar.

    Returns:
        [Row]: searchbar
    """
    return dbc.Row(
        [
            dbc.Col(dbc.Input(type="search", placeholder="Search")),
            dbc.Col(
                dbc.Button(
                    "Search", color="primary", className="ms-2", n_clicks=0
                ),
                width="auto",
            ),
        ],
        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        align="center",
    )

def navbar():
    """Create a navbar.

    Returns:
        [Navbar]: navbar
    """
    return dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=NAVBAR_ICON, height="30px")),
                            dbc.Col(dbc.NavbarBrand("Dashboard", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="#",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    searchbar(),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
            ]
        ),
        color = "dark",
        dark = True,
    )

def content():
    """get the content

    Returns:
        [Div]: view content
    """
    return html.Div([
        dbc.Row([
            dbc.Tabs([
                dbc.Tab(rate_content(), label="Rate", label_style = {"color": "#495057"}),
                dbc.Tab(histogram_content(), label="Prices' histogram",
                        label_style = {"color": "#495057"}),
                dbc.Tab(prices_content(), label="Prices' graph",
                        label_style = {"color": "#495057"}),
            ]),
        ]),
        dbc.Row([
            dbc.Col(html.H1("Map montrant la popularité du bitcoin dans le monde"),
                    width={"size": 12, "offset": 2}),
            map_content(),
        ]),
        dcc.Interval(id='updating', n_intervals=0, interval=5000)
    ])

def rate_content():
    """get rate tab content

    Returns:
        [Card]: rate content
    """
    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                    [
                        dbc.CardImg(
                            src="../assets/img/bitcoin.png",
                            top=True,
                            style={"width": "4rem"},
                        ),

                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.P("7 days :")
                                ]),

                                dbc.Col([
                                    dcc.Graph(id='indicator-bitcoin', figure={},
                                            config={'displayModeBar':False})
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='graph-bitcoin', figure={},
                                            config={'displayModeBar':False})
                                ])
                            ])
                        ]),
                    ],
                    style={"width": "24rem"},
                    className="mt-3"
                ), width=4),
                dbc.Col(
                    dbc.Card(
                    [
                        dbc.CardImg(
                            src="../assets/img/ethereum.png",
                            top=True,
                            style={"width": "4rem"},
                        ),

                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.P("7 days :")
                                ]),

                                dbc.Col([
                                    dcc.Graph(id='indicator-ethereum', figure={},
                                            config={'displayModeBar':False})
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='graph-ethereum', figure={},
                                            config={'displayModeBar':False})
                                ])
                            ])
                        ]),
                    ],
                    style={"width": "24rem"},
                    className="mt-3"
                ), width=4),
                dbc.Col(
                    dbc.Card(
                    [
                        dbc.CardImg(
                            src="../assets/img/litecoin.png",
                            top=True,
                            style={"width": "4rem"},
                        ),

                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.P("7 days :")
                                ]),

                                dbc.Col([
                                    dcc.Graph(id='indicator-litecoin', figure={},
                                            config={'displayModeBar':False})
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='graph-litecoin', figure={},
                                            config={'displayModeBar':False})
                                ])
                            ])
                        ]),
                    ],
                    style={"width": "24rem"},
                    className="mt-3"
                ), width=4),
            ]),
        ])
    )

def histogram_content():
    """Get histogram content.

    Returns:
        [Graph]: content
    """
    return dcc.Graph(id = 'histogram', figure ={})

def prices_content():
    """Get prices graph.

    Returns:
        [Card]: content
    """
    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                    [
                        dbc.CardImg(
                            src="../assets/img/bitcoin.png",
                            top=True,
                            style={"width": "4rem"},
                        ),

                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='prices-bitcoin', figure={},
                                            config={'displayModeBar':False})
                                ])
                            ])
                        ]),
                    ],
                    style={"width": "24rem"},
                    className="mt-3"
                ), width=4),
                dbc.Col(
                    dbc.Card(
                    [
                        dbc.CardImg(
                            src="../assets/img/ethereum.png",
                            top=True,
                            style={"width": "4rem"},
                        ),

                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='prices-ethereum', figure={},
                                            config={'displayModeBar':False})
                                ])
                            ])
                        ]),
                    ],
                    style={"width": "24rem"},
                    className="mt-3"
                ), width=4),
                dbc.Col(
                    dbc.Card(
                    [
                        dbc.CardImg(
                            src="../assets/img/litecoin.png",
                            top=True,
                            style={"width": "4rem"},
                        ),

                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(id='prices-litecoin', figure={},
                                            config={'displayModeBar':False})
                                ])
                            ])
                        ]),
                    ],
                    style={"width": "24rem"},
                    className="mt-3"
                ), width=4),
            ]),
        ])
    )

def map_content():
    """Get the map.

    Returns:
        [Div]: content
    """
    data = get_markers('map_markers.json')
    values = [data[key][0] for key in data.keys()]
    radius = [i[0] for i in values]
    positions = [i[1] for i in values]
    markers = dl.MarkerClusterGroup(id="markers",
                                    children = [dl.CircleMarker(center=pos, radius = rad)
                                                for pos, rad in zip(positions, radius)])
    return dbc.Col(html.Div(dl.Map([
                    dl.TileLayer(),
                    markers,
                    ], style={'width': '1000px', 'height': '500px'})),
                    width={"size": 12, "offset": 2},
    )
