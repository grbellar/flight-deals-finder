from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
from database_setup import db, User
from server import app
import pprint

# TODO add support for layovers (non-direct flights)

# This new search logic should read something like, "for every User in database, search for their cheap flights, if found, email User."
with app.app_context():
    users = db.session.query(User).all()
    for user in users:
        print(user.email)
        for flight in user.flights:
            new_search = FlightSearch()
            search_data = new_search.search_for_flights(flight.departing, flight.destination, flight.price)
            for flight in search_data:
                if flight != "NONE":
                    if flight['data'][0]['price'] <= flight["my_price"]:
                        structured_data = FlightData(flight).get_dict()
                        pprint.pprint(structured_data)
                        current_user = user.email
                        send_notification = NotificationManager(structured_data).send_email_notification(current_user)



