import json
import os
from datetime import *
from dotenv import load_dotenv
from requests import *
from search import GetUserData
from datetime import *
from notification import Notification
from time import *
search = GetUserData()
notification = Notification()
load_dotenv('.env')

class FlightData:
    def shorten_url(self, url):
        """Shortens the long ass url that tequila api gives us."""
        bitly_api_key = os.getenv('BITLY_API_KEY')
        endpoint = 'https://api-ssl.bitly.com/v4/shorten'
        header = {
            'Authorization': bitly_api_key
        }
        parameter = {
            'long_url': url
        }
        r = post(url=endpoint, headers=header, json=parameter).json()['link']
        return r

    def get_flight_data(self, fly_from: str, fly_to: str, date_from: str, date_to: str):
        """Gets flight data from the Tequila API and returns the flight route"""
        load_dotenv('.env')
        tequila_api_key = os.getenv('TEQUILA_API_KEY')
        endpoint = 'https://tequila-api.kiwi.com/v2/search'
        header = {
            'apikey': tequila_api_key
        }
        parameters = {
            'fly_from': fly_from.upper(),
            'fly_to': fly_to.upper(),
            'date_from': date_from,
            'date_to': date_to,
            'adults': 2,
            'flight_type': 'round',
            'one_for_city': 0,
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 28,
            'curr': 'USD',
            'select_airlines': 'f9',
            'select_airlines_exclude': True
        }
        r = get(url=endpoint, headers=header, params=parameters).json()['data'][0]
        route = [i for i in r['route']]
        return [r, route]

    def format_time(self, time_input):
        """Formats time into strftime"""
        formatted_time = datetime.fromisoformat(time_input[:-1]).strftime('%a %d %b - %H:%m')
        return formatted_time

    def organize_data(self, url_input: str, r, route, format_time):
        """Takes flight data and arses it out into the SMS format."""
        flight_path = [i['flyFrom'] for i in route]
        fly_from = r['flyFrom']
        fly_to = r['flyTo']
        nights_in_destination = r['nightsInDest']
        leave_date = format_time(route[0]['local_departure'])
        return_date = format_time(route[-1]['local_arrival'])
        if url_input == 'long':
            url = r['deep_link']
        elif url_input == 'short':
            url = self.shorten_url(url=r['deep_link'])

        price = r['price']

        data_organized = f"\nFrom {fly_from} to {fly_to}\n" \
                         f"Via: {flight_path}\n" \
                         f"Depart: {leave_date} - Return: {return_date}\n" \
                         f"Nights in destination: {nights_in_destination}\n" \
                         f"Price for 2 adults: ${price} USD.\n" \
                         f"{url}"
        return data_organized

    def get_latest(self, today_date_str, future_date_str):
        """Gets users watchlist locations and returns the latest data to console."""
        for i in search.get_user_data('iata'):
            data = self.get_flight_data(fly_from=search.get_user_data('home'),
                                        fly_to=i, date_from=today_date_str,
                                        date_to=future_date_str)
            r = data[0]
            route = data[1]
            print(self.organize_data(url_input='long', r=r, route=route, format_time=self.format_time))

    def time_till(self, days: int, hours: int, minutes: int, seconds: int):
        """Calculates the time till a specific time."""
        t1 = (datetime.now() + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds))
        seconds_till = (t1 - datetime.now()).seconds
        return seconds_till

    def auto_check(self, today_date_str, future_date_str, send_to, day: int, hour):
        """Waits for the x amount of time user sets to check for updates on flight deals and will send SMS message if
        meets user criteria."""
        destinations = search.get_user_data('locations')
        with open('destination.json') as f:
            info = json.load(f)
        t = self.time_till(days=day, hours=hour, minutes=0, seconds=0)
        while True:
            counter = 0
            sleep(t)
            for i in search.get_user_data('iata'):
                data = self.get_flight_data(fly_from=search.get_user_data('home'),
                                            fly_to=i, date_from=today_date_str,
                                            date_to=future_date_str)
                r = data[0]
                route = data[1]
                price = int(r['price'])
                if price <= info['location'][destinations[counter]]['cut off price']:
                    message = f"\nAlert! A prices have dropped!\n{self.organize_data(url_input='short', r=r, route=route, format_time=self.format_time)}"
                    notification.send_text(message=message, to=send_to)
                counter += 1
            print('this ran')



