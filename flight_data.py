# TODO: it would be handy to include the airline as well. would allow a quick glance at the text to see all relevant
#  information and find flight if desired. maybe remove booking link from text?

class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, flight_data: dict):
        self.data = flight_data
        self.depart_city = flight_data["data"][0]["cityFrom"]
        self.depart_code = flight_data["data"][0]["flyFrom"]
        self.arrival_city = flight_data["data"][0]["cityTo"]
        self.arrival_code = flight_data["data"][0]["flyTo"]
        self.price = f"${flight_data['data'][0]['price']}"
        self.leave_flight = flight_data["data"][0]["route"][0]
        self.return_flight = flight_data["data"][0]["route"][1]
        self.utc_leave_date = self.leave_flight["utc_departure"].split("T")[0]
        self.utc_return_date = self.return_flight["utc_departure"].split("T")[0]
        self.link_to_book = flight_data["data"][0]["deep_link"]

    def get_dict(self):
        data_dict = {
            "depart_city": self.depart_city,
            "depart_code": self.depart_code,
            "arrival_city": self.arrival_city,
            "arrival_code": self.arrival_code,
            "price": self.price,
            "utc_leave_date": self.utc_leave_date,
            "utc_return_date": self.utc_return_date,
            "link_to_book": self.link_to_book,
        }
        return data_dict
