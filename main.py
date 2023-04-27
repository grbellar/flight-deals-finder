from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
from database_setup import db, User, FlightTrack
from server import app
import pprint

# TODO add support for layovers (non-direct flights)
# TODO add support for multiple leave locations, like ICT and STL for us poor Wichita folks.
# TODO add support for user to enter their destination and desired flight price

# This new search logic should read something like, "for every User in database, search for their cheap flights, if found, email User."
search_list = []
with app.app_context():
    users = db.session.query(User).all()
    for user in users:
        print(user.email)
        for flight in user.flights:
            search_list.append((flight.destination, flight.price))  # this creates the city_price_tup data structure that FlightSearch is expecting
        new_search = FlightSearch()
        new_search.get_iata_codes(search_list)
        search_data = new_search.search_for_flights()
        for flight in search_data:
            if flight != "NONE":
                if flight['data'][0]['price'] <= flight["my_price"]:
                    structured_data = FlightData(flight).get_dict()
                    pprint.pprint(structured_data)
                    # I believe this currently sends an email to all users for every cheap flight found.
                    # TODO This will need to be re-worked completely to only send to user that is tied to the 
                    # cheap flight. Relational databases should make this easy.
                    # for i in range(len(user_accounts["users"])):
                    #     current_user = user_accounts["users"][i]["email"]
                    #     send_notification = NotificationManager(structured_data).send_email_notification(current_user)
        search_list.clear()



