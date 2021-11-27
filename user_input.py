import os
import sys
from save_data import SaveData
from get_iata_code import GetIataCode

class UserInput:
    def __init__(self):
        self.save_data = SaveData()
        self.get_iata_code = GetIataCode()

    def add_location(self):
        while True:
            """Adding city"""
            while True:
                add_city = input('What is the name of the city you would like to add?\n').lower()

                try:
                    add_city = float(add_city)
                except ValueError:
                    check_city = input(f'You added the city {add_city.title()}. Is that correct? Yes/No\n').lower()
                else:
                    print('That is not a correct response. Try again.')
                    continue
                if check_city == 'yes' or check_city == 'no':
                    if check_city == 'yes':
                        break
                    else:
                        continue
                else:
                    print('That is not a correct response. Try again.')
                    continue
            """Adding IATA code"""
            while True:
                add_iata_code = self.get_iata_code.get_iata_code(city=add_city).upper()

                if not add_iata_code:
                    print(f'No IATA Code found for {add_city.title()}. Try again.')
                    continue
                else:
                    check_iata_code = input(f'The IATA code for {add_city.title()} is {add_iata_code}. '
                                            f'Does that look correct? Yes/No\n').lower()
                if check_iata_code == 'yes' or check_iata_code == 'no':
                    if check_iata_code == 'yes':
                        break
                    else:
                        while True:
                            add_iata_code = input(f'What is the IATA code for {add_city.title()}?\n').lower()
                            check_iata_code = input(f'The IATA code for {add_city.title()} is {add_iata_code.upper()}. '
                                                    f'Does that look correct? Yes/No\n').lower()
                            if check_iata_code == 'yes' or check_iata_code == 'no':
                                if check_iata_code == 'yes':
                                    break
                                else:
                                    continue
                else:
                    print('That is not a correct response. Try again.')
                    continue
            """Adding cut off price"""
            while True:
                add_cut_off_price = input(
                    f'What is the cut off price for {add_city.title()} {add_iata_code.upper()}?\n')
                try:
                    add_cut_off_price = int(add_cut_off_price)
                except ValueError:
                    print('That is not a correct response. Try again.')
                    continue
                else:
                    check_cut_off_price = input(
                        f'You added the cut off price ${add_cut_off_price}. Is that correct? Yes/No\n').lower()
                if check_cut_off_price == 'yes' or check_cut_off_price == 'no':
                    if check_cut_off_price == 'yes':
                        add_cut_off_price = int(add_cut_off_price)
                        break
                    else:
                        continue
                else:
                    print('That is not a correct response. Try again.')
                    continue
            while True:
                check_location_correct = input(f'You have added {add_city.title()} {add_iata_code.upper()} '
                                               f'with the cut off price of ${add_cut_off_price} '
                                               f'Is this correct? Yes/No\n')
                if check_location_correct == 'yes' or check_location_correct == 'no':
                    if check_location_correct == 'yes':

                        """Saves data"""
                        location_data = {'add_location': [add_city, add_iata_code,
                                                          add_cut_off_price]}
                        self.save_data.save_data(save_type=location_data)
                        break
                    else:
                        break
                else:
                    print('That is not a correct response. Try again.')
                    continue
            if check_location_correct == 'no':
                continue
            """Add another location?"""
            while True:
                add_another_location = input('Would you like to add another city? Yes/No \n').lower()
                if add_another_location == 'yes' or add_another_location == 'no':
                    if add_another_location == 'yes':
                        break
                    else:
                        return
                else:
                    print('That is not a correct response. Try again.')
                    continue

    def add_home(self, user_home):
        while True:
            while True:
                check_user_home = input(
                    f'Your current home is set to {user_home}. Would you like to update it? Yes/No\n').lower()
                if check_user_home == 'yes' or check_user_home == 'no':
                    if check_user_home == 'yes':
                        break
                    else:
                        break
                else:
                    print('That is not a correct response. Try again.')
                    continue
            if check_user_home == 'no':
                break
            else:
                while True:
                    add_user_home = input(f'What is the IATA code you would like to add as your home city?\n').upper()
                    try:
                        add_user_home = float(add_user_home)
                    except ValueError:
                        check_correct = input(
                            f'Your home has been updated to {add_user_home.upper()}. Is that correct? Yes/No\n').lower()
                    else:
                        print('That is not a correct response. Try again.')
                        continue
                    if check_correct == 'yes' or check_correct == 'no':
                        if check_correct == 'yes':
                            """Save new home data"""
                            location_data = {'add_home': add_user_home}
                            self.save_data.save_data(save_type=location_data)
                            break
                        else:
                            continue
                    else:
                        print('That is not a correct response. Try again.')
                        continue
                if check_correct == 'yes':
                    break
