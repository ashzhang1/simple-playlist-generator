import requests
import json
from secrets import refresh_token, base_64


class refresh:
    def __init__(self):
        self.refresh_token = refresh_token
        self.base_65 = base_64

    def refresh(self):

        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query, data = {"grant_type": "refresh_token", "refresh_token": refresh_token, },
                                 headers={"Authorization": "Basic " + base_64})

        return response.json()["access_token"]

