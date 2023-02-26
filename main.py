from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
# TODO: add support for layovers (non-direct flights)
# TODO: add support for multiple leave locations, like ICT and STL for us poor Wichita folks.
# TODO: add support for user to enter their destination and desired flight price
# TODO: schedule this to run as a cron job :):)

data_manager = DataManager()
user_accounts = data_manager.get_sheet_user_data()

city_price_tup = data_manager.get_city_price()
new_search = FlightSearch()
new_search.get_iata_codes(city_price_tup)
search_data = new_search.search_for_flights()
#
# search data is a list of individual flight searches. one search object for each valid city in google sheet.
for flight in search_data:
    if flight != "NONE":
        if flight['data'][0]['price'] <= flight["my_price"]:
            structured_data = FlightData(flight).get_dict()
            # print("cheap flight!")
            for i in range(len(user_accounts["users"])):
                current_user = user_accounts["users"][i]["email"]
                send_notification = NotificationManager(structured_data).send_email_notification(current_user)
    #     else:
    #         print("price did not meet lowest price requirement")
    # else:
    #     print("no flights found")

