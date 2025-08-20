import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self._user = os.getenv("SHEETY_USERNAME")
        self._password = os.getenv("SHEETY_PASSWORD")
        self.prices_endpoint = os.getenv("SHEETY_PRICES_ENDPOINT")
        self.users_endpoint = os.getenv("SHEETY_USERS_ENDPOINT")
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        # Use Sheety API to GET all the data in the sheet and print it out
        response = requests.get(url=self.prices_endpoint, auth=self._authorization)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price":{
                    "iataCode": city['iataCode']
                    }
                }
            response = requests.put(
                url=f"{self.prices_endpoint}/{city['id']}",
                json=new_data,
                auth=self._authorization
            )
            print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint, auth=self._authorization)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data