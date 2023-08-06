# from setuptools import setup
import requests


class Weather:
    """Creates a Weather object getting an apikey as input
    and either a City name OR Latitude & Longitude coordinates.

    Package use example:

    # Create a weather object using a city name:
    # Get your own apikey from https://openweathermap.org
    # And wait a couple of hours for the apikey to be activated

    >> weather = Weather(apikey="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", city="London")

    # Using Latitude and Longitude coordinates:
    >> weather = Weather(apikey="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", lat=40.1, lon=3.4)

    # Get complete weather data for the next 12 hours:
    >> weather.next_12h()

    # Simplified data for the next 12 hours:
    >> weather.next_12h_simplified()

    """
    def __init__(self, apikey, city=None, lat=None, lon=None):
        self.apikey = apikey
        self.city = city
        self.lat = lat
        self.lon = lon

        if self.city:
            url = f"http://api.openweathermap.org/data/2.5/forecast?" \
                  f"q={self.city}&" \
                  f"appid={self.apikey}&" \
                  f"units=metric"
            r = requests.get(url)
            self.data = r.json()
        elif self.lat and self.lon:
            url = f"http://api.openweathermap.org/data/2.5/forecast?" \
                  f"lat={self.lat}&" \
                  f"lon={self.lon}&" \
                  f"appid={self.apikey}&" \
                  f"units=metric"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("Provide either a City OR Latitude & Longitude!")

        if self.data["cod"] != "200":
            raise ValueError(self.data["message"])

    def next_12h(self):
        """Returns 3-hour data for the next 12 hours as a dict.
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """Returns date, temperature and sky condition every 3 hours
        for the next 12 hours as a tuple of tuples.
        """
        simple_data = []
        for data_list in self.data['list'][:4]:
            simple_data.append((data_list['dt_txt'], data_list['main']['temp'], data_list['weather'][0]['description']))
        return simple_data
