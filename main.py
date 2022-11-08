import os
from datetime import *
from threading import Thread
from dotenv import load_dotenv
from flight_data import FlightData
from search import GetUserData
from user_input import UserInput

send_to = os.getenv('PHONENUMBER')
notification_day = 1
notification_hour = 8
search = GetUserData()
flight_data = FlightData()
user_input = UserInput()

running = True
load_dotenv('.env')
today_date = datetime.now()
today_date_str = today_date.strftime('%d/%m/%Y')
days_in_future = 180
future_date = today_date + timedelta(days=days_in_future)
future_date_str = future_date.strftime('%d/%m/%Y')


def future_date(today_date, days_in_future):
    """Gets the date in x amount of days"""
    future_date_str = (today_date + timedelta(days=days_in_future)).strftime('%d/%m/%Y')
    return future_date_str

def user_menu():
    """Helps user navigate features of app"""
    global running
    user_options = ['add location', 'change home', 'get latest', 'change cutoff']

    while running:
        """Intro"""
        user_text_input = input('What would you like to do today? Type (help) for options. \n').lower()
        if user_text_input == 'help':
            print(user_options)
            continue
        elif user_text_input not in user_options:
            print('That is not a valid response. Try again.')
            continue
        elif user_text_input in user_options:
            """menu items"""
            if user_text_input == user_options[0]:
                """adding location"""
                user_input.add_location()
            elif user_text_input == user_options[1]:
                """changing home"""
                user_input.add_home(user_home=search.get_user_data(search='home'))
            elif user_text_input == user_options[2]:
                """Get latest"""
                data = flight_data.get_latest(today_date_str=today_date_str,
                                              future_date_str=future_date_str)
            elif user_text_input == user_options[3]:
                """Update cutoff price"""
                pass
            else:
                print(user_options)
        else:
            print('error with user input.')


b = Thread(name='background', target=flight_data.auto_check, args=(today_date_str, future_date_str, send_to,
                                                                   notification_day, notification_hour))


def start():
    """Main function that starts apps flight checking background"""
    global running
    while running:
        b.start()
        user_menu()


f = Thread(name='forground', target=start)

f.start()















