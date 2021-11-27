from datetime import *
import json
import os
from dotenv import load_dotenv
from twilio.rest import Client
from user_input import UserInput
from flight_data import FlightData
from search import GetUserData

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
address_book = [os.getenv('SYDNEY'), os.getenv('JACOB')]
"""
Features
a list of places I want to go. with ability to expand that list and update the lowest price
# destination = {
#     'home': 'SLC',
#     'location': {
#         'new york': {
#             'iata code': None,
#             'lowest price': None,
#             'historical price': {
#                 'date': {
#                     '20211124': {
#                         'price': []
#                     }
#                 }
#             }
#         }
#     }
# }
price cut off of the max id pay for that location
send text if it hits that cut off price with the location, airline, date and url to book it

Flow
user opens program
user adds city and iata code and max price
computer keeps asking if there are any other to add
after list is created computer gets the flight data
checks if it meets the cut off if it does sends a notification

 (dd/mm/yyyy)
"""


def future_date(today_date, days_in_future):
    future_date_str = (today_date + timedelta(days=days_in_future)).strftime('%d/%m/%Y')
    return future_date_str


def exit(exit):
    global running
    if exit == 'exit':
        running = False
        print('Closing down program.')
    return running

# print(search.get_user_data('home'))
# print(type(search.get_user_data('home')))
# print(flight_data.get_flight_data(fly_from='slc', fly_to='HEL', date_from=today_date_str, date_to=future_date_str))


def user_menu():
    user_options = ['add location', 'change home', 'exit', 'get latest']
    while running:
        """Intro"""
        user_text_input = input('What would you like to do today? Type (help) for options. \n').lower()
        if user_text_input == 'help':
            print(user_options)
            continue
        elif user_text_input not in user_options:
            print('that is not a valid response. Try again.')
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
                """exit program"""
                exit(exit='exit')
                break
            elif user_text_input == user_options[3]:
                flight_data.get_latest(today_date_str=today_date_str,
                                       future_date_str=future_date_str)

        else:
            print('error with user input.')


def send_text(message, to):
    twilio_sid = os.getenv('TWILIO_SID')
    twilio_token = os.getenv('TWILIO_TOKEN')
    client = Client(twilio_sid, twilio_token)
    message_info = client.messages.create(body=message, from_='+13155644341', to=f'+1{to}')
    return message_info.sid


def start():
    global running

    while running:
        user_menu()


"""Whats the problem
the for loop is running 4 times

"""
user_menu()