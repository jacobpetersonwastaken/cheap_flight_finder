import os
from requests import *
from dotenv import load_dotenv


class GetIataCode:

    def get_iata_code(self, city: str):
        load_dotenv('.env')
        location_endpoint = f'https://tequila-api.kiwi.com/locations/query'
        tequila_api_key = os.getenv('TEQUILA_API_KEY')
        header = {
            'apikey': tequila_api_key
        }
        query = {
            "term": city,
            "location_types": "city",
            'limit': 10
        }
        r = get(url=location_endpoint, headers=header, params=query)
        results = r.json()["locations"]
        if len(results) == 0:
            return False
        else:
            code = results[0]["code"]
            return code

