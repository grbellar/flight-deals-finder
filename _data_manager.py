import requests
from dotenv import load_dotenv
import os
from database_setup import db, User, FlightTrack

load_dotenv(".env")


class DataManager:

    def __init__(self):
        pass
        # self.price_endpoint = "https://api.sheety.co/e06af66708839e6bf52c725e0c87c755/flightDeals/prices"
        # self.user_endpoint = "https://api.sheety.co/e06af66708839e6bf52c725e0c87c755/flightDeals/users"
        # self.sheety_headers = {
        #     "Authorization": os.environ.get("SHEETY_TOKEN"),
        # }

    # def get_sheet_flight_data(self):
    #     response = requests.get(url=self.price_endpoint, headers=self.sheety_headers)
    #     response.raise_for_status()
    #     data = response.json()
    #     return data

    # Can likely delete this method entirely. See todo in main.py
    def get_sheet_user_data(self):
        response = requests.get(url=self.user_endpoint, headers=self.sheety_headers)
        response.raise_for_status()
        data = response.json()
        return data

    def get_city_price(self):
        response = requests.get(url=self.price_endpoint, headers=self.sheety_headers)
        response.raise_for_status()
        data = response.json()
        city_price_tuple = [(city["city"], city["lowestPrice"]) for city in data["prices"]]
        return city_price_tuple
