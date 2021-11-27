import os
from datetime import *
from dotenv import load_dotenv
from requests import *
from search import GetUserData

search = GetUserData()


class FlightData:
    def __init__(self):
        load_dotenv('.env')

    def shorten_url(self, url):
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

        def format_time(time_input):
            formatted_time = datetime.fromisoformat(time_input[:-1]).strftime('%a %d %b - %H:%m')
            return formatted_time

        flight_path = [i['flyFrom'] for i in route]
        fly_from = r['flyFrom']
        fly_to = r['flyTo']
        nights_in_destination = r['nightsInDest']
        leave_date = format_time(route[0]['local_departure'])
        return_date = format_time(route[-1]['local_arrival'])
        url_shorten = self.shorten_url(url=r['deep_link'])
        url = r['deep_link']
        price = r['price']

        data_organized = f"\nFrom {fly_from} to {fly_to}\n" \
                         f"Via: {flight_path}\n" \
                         f"Depart: {leave_date} - Return: {return_date}\n" \
                         f"Nights in destination: {nights_in_destination}\n" \
                         f"Price for 2 adults: ${price} USD.\n" \
                         f"{url}"
        return data_organized

    def get_latest(self, today_date_str, future_date_str):
        for i in search.get_user_data('iata'):
            print(self.get_flight_data(fly_from=search.get_user_data('home'),
                                       fly_to=i, date_from=today_date_str,
                                       date_to=future_date_str))
