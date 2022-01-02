"""[Summary] :  heart of the app, launch the server."""

#============================================================================

# Created By   :  Marwan MEZROUI, Rayan SOBH, Etienne CHEVET
# Last Update  :  02/01/2022
# Version      :  1.0

#============================================================================
import os
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from views import home
from models.data import DataCryptoGenerator
from models.data import DataMapGenerator
from models.data import get_market_caps
from models.data import get_prices
from models.data import get_dataframe
from models.data import generate_markers
from utils import tools

#-- SETTING DATA --#
# check if crypto data file exist, create it if it doesn't
try:
    f = open(os.getcwd() + '/models/data.json', encoding='utf-8')
except IOError:
    generator = DataCryptoGenerator()
    generator.add_crypto('bitcoin', 'usd')
    generator.add_crypto('ethereum', 'usd')
    generator.add_crypto('litecoin', 'usd')
    generator.generate_json('data.json')
finally:
    f.close()

# get market_caps data
bitcoin_marketcaps = get_market_caps('data.json', 'bitcoin')
ethereum_marketcaps = get_market_caps('data.json', 'ethereum')
litecoin_marketcaps = get_market_caps('data.json', 'litecoin')

# get prices data with date
bitcoin_prices = get_prices('data.json', 'bitcoin', False)
ethereum_prices = get_prices('data.json', 'ethereum', False)
litecoin_prices = get_prices('data.json', 'litecoin', False)

# get prices data with datetime
bitcoin_prices_time = get_prices('data.json', 'bitcoin', True)
ethereum_prices_time = get_prices('data.json', 'ethereum', True)
litecoin_prices_time = get_prices('data.json', 'litecoin', True)

# check if map data file exist, create it if it doesn't
try:
    f = open(os.getcwd() + '/models/map_data.json', encoding='utf-8')
except IOError:
    generator = DataMapGenerator()
    generator.add_keyword('bitcoin')
    generator.add_keyword('ethereum')
    generator.add_keyword('litecoin')
    generator.generate_json('map_data.json')
finally:
    f.close()

# get map data
map_data_bitcoin = get_dataframe('map_data.json', 'bitcoin')
map_data_bitcoin = map_data_bitcoin[map_data_bitcoin.popularity > 0]


# check if markers data file exist, create it if it doesn't
try:
    f = open(os.getcwd() + '/models/map_markers.json', encoding='utf-8')
except IOError:
    generate_markers('map_markers.json', map_data_bitcoin)
finally:
    f.close()

#============================================================================

#-- SETTING APP --#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "My Dashboard"
app._favicon = "img/logo.png"
app.layout = home.render()

#============================================================================

#-- CALLBACKS AREA --#
# FIRST ROW - FIRST TAB
@app.callback(
    Output('indicator-bitcoin', 'figure'),
    Input('updating', 'n_intervals')
)
def update_indicator_bitcoin(timer):
    """Update market caps indicator for bitcoin.

    Args:
        timer (int): interval

    Returns:
        [fig]: indicator
    """
    return tools.update_indicator(bitcoin_marketcaps)

@app.callback(
    Output('graph-bitcoin', 'figure'),
    Input('updating', 'n_intervals')
)
def update_graph_bitcoin(timer):
    """Update bitcoin graph about market caps.

    Args:
        timer (int): interval

    Returns:
        [fig]: graph
    """
    return tools.update_graph(bitcoin_marketcaps)

@app.callback(
    Output('indicator-ethereum', 'figure'),
    Input('updating', 'n_intervals')
)
def update_indicator_ethereum(timer):
    """Update market caps indicator for ethereum.

    Args:
        timer (int): interval

    Returns:
        [fig]: indicator
    """
    return tools.update_indicator(ethereum_marketcaps)

@app.callback(
    Output('graph-ethereum', 'figure'),
    Input('updating', 'n_intervals')
)
def update_graph_ethereum(timer):
    """Update ethereum graph about market caps.

    Args:
        timer (int): interval

    Returns:
        [fig]: graph
    """
    return tools.update_graph(ethereum_marketcaps)

@app.callback(
    Output('indicator-litecoin', 'figure'),
    Input('updating', 'n_intervals')
)
def update_indicator_litecoin(timer):
    """Update market caps indicator for litecoin.

    Args:
        timer (int): interval

    Returns:
        [fig]: indicator
    """
    return tools.update_indicator(litecoin_marketcaps)

@app.callback(
    Output('graph-litecoin', 'figure'),
    Input('updating', 'n_intervals')
)
def update_graph_litecoin(timer):
    """Update litecoin graph about market caps.

    Args:
        timer (int): interval

    Returns:
        [fig]: graph
    """
    return tools.update_graph(litecoin_marketcaps)

# FIRST ROW - SECOND TAB
@app.callback(
    Output('histogram', 'figure'),
    Input('updating', 'n_intervals')
)
def update_histogram(timer):
    """Update histogram.

    Args:
        timer (int): interval

    Returns:
        [fig]: histogram
    """
    return tools.update_histogram(tools.concat([bitcoin_prices, ethereum_prices, litecoin_prices]))

# FIRST ROW - THIRD TAB
@app.callback(
    Output('prices-bitcoin', 'figure'),
    Input('updating', 'n_intervals')
)
def update_bitcoin_prices(timer):
    """Update bitcoin graph about prices.

    Args:
        timer (int): interval

    Returns:
        [fig]: graph
    """
    return tools.update_prices(bitcoin_prices_time, 'red')

@app.callback(
    Output('prices-ethereum', 'figure'),
    Input('updating', 'n_intervals')
)
def update_ethereum_prices(timer):
    """Update ethereum graph about prices.

    Args:
        timer (int): interval

    Returns:
        [fig]: graph
    """
    return tools.update_prices(ethereum_prices_time, 'purple')

@app.callback(
    Output('prices-litecoin', 'figure'),
    Input('updating', 'n_intervals')
)
def update_litecoin_prices(timer):
    """Update litecoin graph about prices.

    Args:
        timer (int): interval

    Returns:
        [fig]: graph
    """
    return tools.update_prices(litecoin_prices_time, 'pink')

#============================================================================

#-- SERVER RUN AREA --#
if __name__ == '__main__':
    app.run_server()
