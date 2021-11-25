class UserInput:

    def add_location(self, save_data):
        while True:
            """Adding city"""
            while True:
                add_city = input('What is the name of the city you would like to add?\n').lower()
                try:
                    add_city = float(add_city)
                except ValueError:
                    check_correct = input(f'You added the city {add_city.title()}. Is that correct? Yes/No\n').lower()
                else:
                    print('That is not a correct response. Try again.')
                    continue
                if check_correct == 'yes' or check_correct == 'no':
                    if check_correct == 'yes':
                        break
                    else:
                        continue
                else:
                    print('That is not a correct response. Try again.')
                    continue
            """Adding IATA code"""
            while True:
                add_iata_code = input(f'What is the IATA code for {add_city.title()}?\n').lower()
                try:
                    add_iata_code = float(add_iata_code)
                except ValueError:
                    check_correct = input(f'You added the IATA code {add_iata_code.upper()}. '
                                          f'Is that correct? Yes/No\n').lower()
                else:
                    print('That is not a correct response. Try again.')
                    continue
                if check_correct == 'yes' or check_correct == 'no':
                    if check_correct == 'yes':
                        break
                    else:
                        continue
                else:
                    print('That is not a correct response. Try again.')
                    continue
            """Adding cut off price"""
            while True:
                add_cut_off_price = input(f'What is the cut off price for {add_city.title()} {add_iata_code.upper()}?\n')
                try:
                    add_cut_off_price = int(add_cut_off_price)
                except ValueError:
                    print('That is not a correct response. Try again.')
                    continue
                else:
                    check_correct = input(
                        f'You added the cut off price ${add_cut_off_price}. Is that correct? Yes/No\n').lower()
                if check_correct == 'yes' or check_correct == 'no':
                    if check_correct == 'yes':
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
                        save_data()
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

    def add_home(self, save_data, user_home):
        while True:
