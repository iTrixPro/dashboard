"""[Summary] :  others class or functions that can be useful."""

#============================================================================

# Created By   :  Marwan MEZROUI, Rayan SOBH, Etienne CHEVET
# Last Update  :  02/01/2022
# Version      :  1.0

#============================================================================
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from geopy.geocoders import Nominatim

def update_indicator(data):
    """Draw indicator of market caps.

    Args:
        data ([DataFrame): data given

    Returns:
        [fig]: indicator
    """
    starting_rate = data[data.date == data.date.min()].market_caps.values[0]
    ending_rate = data[data.date == data.date.max()].market_caps.values[0]

    fig = go.Figure(go.Indicator(
        mode="delta",
        value=ending_rate,
        delta={'reference': starting_rate, 'relative': True, 'valueformat':'.2%'}))
    fig.update_traces(delta_font={'size':12})
    fig.update_layout(height=30, width=70)
    fig.update_traces(delta_increasing_color='green' if ending_rate >= starting_rate else 'red')

    return fig

def update_graph(data):
    """Draw market caps graph

    Args:
        data (DataFrame): data given

    Returns:
        [fig]: graph
    """
    fig = px.line(data, x='date', y='market_caps',
                   range_y=[data.market_caps.min(), data.market_caps.max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                             paper_bgcolor='rgba(0,0,0,0)',
                                             plot_bgcolor='rgba(0,0,0,0)',
                                             yaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ),
                                             xaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ))

    starting_rate = data[data.date == data.date.min()].market_caps.values[0]
    ending_rate = data[data.date == data.date.max()].market_caps.values[0]
    fig.update_traces(fill='tozeroy')
    return fig.update_traces(line={'color':'green'} if ending_rate >= starting_rate
                             else {'color': 'red'})

def update_histogram(data):
    """Draw histogram according to data.

    Args:
        data (DataFrame): data given

    Returns:
        [fig]: histogram
    """
    fig = px.histogram(data, x = 'date',  y = 'prices', color = 'name',
                       range_x=[data.date.min(), data.date.max()])


    return fig

def update_prices(data, color):
    """Draw graph of evolution of prices according to the date.

    Args:
        data (DataFrame): data given
        color (string): graph color

    Returns:
        [fig]: graph
    """
    fig = px.line(data, x = 'date', y = 'prices')
    fig.update_traces(line={'color': color})
    return fig

def concat(frames):
    """concat different dataframes.

    Args:
        frames (array): array of dataframe

    Returns:
        [DataFrame]: concat result
    """
    return pd.concat(frames)

geolocator = Nominatim(user_agent="http")
def latitude_longitude(country):
    """get latitude and longitude of a country

    Args:
        country (string): country name

    Returns:
        [list]: lat & lon
    """
    localisation = geolocator.geocode(country)
    return [localisation.latitude, localisation.longitude]
