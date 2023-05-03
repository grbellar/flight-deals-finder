import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv("./.env")
today = datetime.now()
six_months_from_now = today + timedelta(days=365)  # nifty way to create new date objects using a specified time frame


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.base_endpoint = "https://tequila-api.kiwi.com"
        self.search_endpoint = "/v2/search"
        self.location_endpoint = "/locations/query"
        self.headers = {
            "accept": "application/json",
            "apikey": os.environ.get("KIWI_API_KEY"),
        }
        self.data = {
            "fly_from": "",
            "fly_to": "",
            "date_from": today.strftime("%d/%m/%Y"),
            "date_to": six_months_from_now.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 3,  # TODO also need to allow user to select time frame. or maybe not?
            "nights_in_dst_to": 8,
            "flight_type": "round",
            "curr": "USD",
            "max_stopovers": 0,
            "limit": 1
        }
        self.search_data = []


    def search_for_flights(self, departing, destination, desired_price):
        self.data["fly_from"] = departing
        self.data["fly_to"] = destination
        response = requests.get(url=f"{self.base_endpoint}{self.search_endpoint}",
                                headers=self.headers,
                                params=self.data)
        response.raise_for_status()
        flight_data = response.json()
        flight_data["my_price"] = desired_price
        if len(flight_data["data"]) < 1:  # if the length of data list is zero (no results found)
            self.search_data.append(f"NONE")
        else:
            self.search_data.append(flight_data)
        return self.search_data
