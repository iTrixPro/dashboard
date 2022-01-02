"""[Summary] :  conversions class or functions."""

#============================================================================

# Created By   :  Marwan MEZROUI, Rayan SOBH, Etienne CHEVET
# Last Update  :  02/01/2022
# Version      :  1.0

#============================================================================
from datetime import datetime

class DateConverter:
    """
    Class which convert the date given into unix time or the opposite.
    """
    @staticmethod
    def date_to_unix(year, month, day):
        """Convert date into unix time.

        Args:
            year (int)
            month (int)
            day (int)

        Returns:
            [float]: unix time
        """
        return (datetime(year, month, day) - datetime(1970, 1, 1)).total_seconds()

    @staticmethod
    def unix_to_date(time):
        """Convert unix time into date.

        Args:
            time (float): unix time

        Returns:
            [date]: date
        """
        time = int(time/1000 if len(str(time)) > 10 else time)
        return datetime.utcfromtimestamp(time).strftime('%d/%m/%Y').lower()

    @staticmethod
    def unix_to_datetime(time):
        """Convert unix time into datetime.

        Args:
            time (float): unix time

        Returns:
            [date]: date
        """
        time = int(time/1000 if len(str(time)) > 10 else time)
        return datetime.utcfromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S").lower()
