import json

class SaveData:
    def save_data(self, save_type):
        print('saving data...')
        with open('destination.json') as f:
            data = json.load(f)
        if 'add_location' in save_type:
            add_city = save_type['add_location'][0]
            add_iata_code = save_type['add_location'][1]
            add_cut_off_price = save_type['add_location'][2]

            # data['locations'][add_city] = {'iata code': add_iata_code,
            #                'cut off price': add_cut_off_price
            #                }
            # data['locations'].append({
            #     add_city: {'iata code': add_iata_code,
            #                'cut off price': add_cut_off_price
            #                }
            # })
            # data['locations'] = [{
            #     add_city: {'iata code': add_iata_code,
            #                'cut off price': add_cut_off_price
            #                }
            # }]

            data['location'][add_city] = {'iata code': add_iata_code,
                                          'cut off price': add_cut_off_price
                                          }

        elif 'add_home' in save_type:
            data['home'] = save_type['add_home']
        with open('destination.json', 'w') as file:
            json.dump(data, file)
        print('Data saved.')