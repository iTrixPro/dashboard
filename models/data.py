"""[Summary] :  file where is handled the creation of the data files."""

#============================================================================

# Created By   :  Marwan MEZROUI, Rayan SOBH, Etienne CHEVET
# Last Update  :  02/01/2022
# Version      :  1.0

#============================================================================
import json
import os
from datetime import date
from datetime import timedelta
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI
from utils.converters import DateConverter
from utils import tools
from pytrends.request import TrendReq


#-- CLASS --#
class DataCryptoGenerator:
    """
    Generator of json file according to the content of the data dict for grahs.
    It will give a json with the prices, markets_caps and datetime or date of a
    crypto.
    """
    cg = CoinGeckoAPI()
    ending_date = date.today()
    starting_date = ending_date - timedelta(days = 7)

    def __init__(self):
        self.data = {}

    def add_crypto(self, crypto_id, currency):
        """Add a crypto in our data dict.

        Args:
            crypto_id (string): id of the crypto (ex: 'bitcoin')
            currency (string): type of currency (ex: 'eur')
        """
        self.data[crypto_id] = DataCryptoGenerator.cg.get_coin_market_chart_range_by_id(
            id = crypto_id,
            vs_currency = currency,
            from_timestamp = DateConverter.date_to_unix(DataCryptoGenerator.starting_date.year,
                                                          DataCryptoGenerator.starting_date.month,
                                                          DataCryptoGenerator.starting_date.day),
            to_timestamp = DateConverter.date_to_unix(DataCryptoGenerator.ending_date.year,
                                                        DataCryptoGenerator.ending_date.month,
                                                        DataCryptoGenerator.ending_date.day)
        )

    def remove_crypto(self, crypto_id):
        """Remove a crypto from our data dict.

        Args:
            crypto_id (string): id of the crypto
        """
        self.data.pop(crypto_id)

    def generate_json(self, filename):
        """Generate the json file.

        Args:
            filename (string): name of the file
        """
        with open(os.getcwd() + '/models/' + filename, 'w+', encoding="utf-8") as file :
            json.dump(self.data, file)


class DataMapGenerator:
    """
    Generator of json file according to the content of the data dict for map.
    It will give a json file given info about the trend of each crypto(given)
    in the world by country to see the popularity of each crypto in the world
    and maybe explain the supremacy of one of those crypto
    """
    def __init__(self):
        self.keywords = []

    def add_keyword(self, keyword):
        """Add keyword in our list

        Args:
            keyword (string): keyword like 'bitcoin'
        """
        self.keywords.append(keyword)

    def generate_json(self, filename):
        """Generate the json file.

        Args:
            filename (string): name of the file
        """
        trend = TrendReq()
        trend.build_payload(self.keywords)
        data = trend.interest_by_region()
        with open(os.getcwd() + '/models/' + filename, 'w+', encoding="utf-8") as file :
            json.dump(json.loads(data.to_json()), file)




#-- FUNCTIONS --#
def get_market_caps(filename, cryptoname):
    """Get rate of crypto given from json file.

    Args:
        filename (string): name of file
        cryptoname (string): crypto's id

    Returns:
        [DataFrame]: rates
    """
    data = pd.read_json(os.getcwd() + '/models/' + filename)
    return pd.DataFrame({'date':[ DateConverter.unix_to_datetime(i[0])
                                    for i in data[cryptoname].market_caps ],
                            'market_caps':np.array(data[cryptoname].market_caps)[:,1] })

def get_prices(filename, cryptoname, datetime):
    """Get crypto prices from json file.

    Args:
        filename (string): name of json file
        cryptoname (string): id of crypto
        datetime (bool): if u want date or datetime

    Returns:
        [DataFrame]: prices
    """
    data = pd.read_json(os.getcwd() + '/models/' + filename)
    if not datetime:
        return pd.DataFrame({'name': cryptoname,
                            'date':[ DateConverter.unix_to_date(i[0])
                                    for i in data[cryptoname].prices ],
                            'prices':np.array(data[cryptoname].prices)[:,1] })

    return pd.DataFrame({'name': cryptoname,
                        'date':[ DateConverter.unix_to_datetime(i[0])
                                for i in data[cryptoname].prices ],
                        'prices':np.array(data[cryptoname].prices)[:,1] })

def get_dataframe(filename, cryptoname):
    """Get DataFrame from filename given and cryptoname given.

    Args:
        filename (string): file name
        cryptoname (string): crypto name

    Returns:
        [DataFrame]: data
    """
    data = pd.read_json(os.getcwd() + '/models/' + filename)
    return pd.DataFrame({'country':[ i for i in data[cryptoname].keys()],
                           'popularity':[ i for i in data[cryptoname]]})

def generate_markers(filename, data):
    """Generate markers json file.

    Args:
        filename (string): file name
        data (DataFrame): data which has the countries name
    """

    markers = {}
    for i,j in zip(data.country, data.popularity):
        markers[str(i)] = [j, tools.latitude_longitude(i)]

    with open(os.getcwd() + '/models/' + filename, 'w+', encoding="utf-8") as file :
        json.dump(markers, file)

def get_markers(filename):
    """Get markers json file.

    Args:
        filename (string): name of file

    Returns:
        [DataFrame]: json file
    """
    return pd.read_json(os.getcwd() + '/models/' + filename, lines=True)
