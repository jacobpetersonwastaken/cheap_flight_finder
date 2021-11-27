from datetime import *
import json
import os
from dotenv import load_dotenv
from requests import *
from twilio.rest import Client
from threading import Thread
from user_input import UserInput

user_input = UserInput()

running = True
load_dotenv('.env')
today_date = datetime.now()
today_date_str = today_date.strftime('%d/%m/%Y')
days_in_future = 90
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


def get_user_data(search):
    with open('destination.json') as f:
        data = json.load(f)
    if search == 'home':
        home = data['home']
        return home


def exit(exit):
    global running
    if exit == 'exit':
        running = False
        print('Closing down program.')
    return running


def user_menu():
    user_options = ['add location', 'change home', 'exit']
    while running:
        user_text_input = input('What would you like to do today? Type (help) for options. \n').lower()
        if user_text_input == 'help':
            print(user_options)
            continue
        elif user_text_input not in user_options:
            print('that is not a valid response. Try again.')
            continue
        elif user_text_input in user_options:
            if user_text_input == user_options[0]:
                """adding location"""
                user_input.add_location()
            elif user_text_input == user_options[1]:
                """changing home"""
                user_input.add_home(user_home=get_user_data(search='home'))
            elif user_text_input == user_options[2]:
                """exit program"""
                exit(exit='exit')
                break
        else:
            print('error with user input.')


user_menu()


def notification(message, to):
    twilio_sid = os.getenv('TWILIO_SID')
    twilio_token = os.getenv('TWILIO_TOKEN')
    client = Client(twilio_sid, twilio_token)
    message_info = client.messages.create(body=message, from_='+13155644341', to=f'+1{to}')
    return message_info.sid


def get_flight_data(from_iata: str, date_from: str, date_to: str, adults: int):

    # nomad_api_key = os.getenv('TEQUILA_NOMAD_API_KEY')
    tequila_api_key = os.getenv('TEQUILA_API_KEY')
    endpoint = 'https://tequila-api.kiwi.com/v2/search'
    nomad_endpoint = 'https://tequila-api.kiwi.com/v2/nomad'
    header = {
        'apikey': tequila_api_key
    }
    parameters = {
        'fly_from': from_iata,
        'fly_to': '40.76--111.89-2000km',
        'date_from': date_from,
        'date_to': date_to,
        'adults': adults,
        'flight_type': 'round',
        'curr': 'USD',
        'price_from': 50,
        'price_to': 700,
        "nights_in_dst_from": 3,
        "nights_in_dst_to": 28
    }
    r = get(url=endpoint, headers=header, params=parameters).json()
    result_list = [i for i in r]
    for i in result_list:
        city = i['cityTo']
        price = i['price']
        print(city, price)



def quit_program():
    global running
    stop = input('To end program type: stop')
    if stop == 'stop':
        running = False
        print('saving all your data...')
    return running


def start():
    global running
    t = Thread(target=user_input)
    t.start()
    while running:
        pass
