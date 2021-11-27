import json


class GetUserData:
    def get_user_data(self, search):
        with open('destination.json') as f:
            data = json.load(f)
        if search == 'home':
            home = data['home']
            return home
        if search == 'locations':
            locations = [i for i in data['location']]
            return locations
        if search == 'iata':
            iata_codes = [data['location'][i]['iata code'] for i in data['location']]
            return iata_codes

