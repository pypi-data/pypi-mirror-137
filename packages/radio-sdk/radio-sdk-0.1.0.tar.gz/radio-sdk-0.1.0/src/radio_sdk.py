# Brendan Mulhern
# 2/4/2022

import requests

class radio_sdk():
    base_url = "https://radio-browser.p.rapidapi.com"
    host = "radio-browser.p.rapidapi.com"
    def __init__(self, api_key: str):
        self.api_key = api_key
    def list_of_country_codes(self, format: str, order: str, reverse: str, hidebroken: str):
        try:
            url = f"{self.base_url}/{format}/countrycodes"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            querystring = {
                "order": order or "stationcount",
                "reverse": reverse or "false",
                "hidebroken": hidebroken or "true"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return response.json()
        except Exception as e:
            return e
    def list_of_codecs(self, format: str, order: str, reverse: str, hidebroken: str):
        try:
            url = f"{self.base_url}/{format}/codecs"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            querystring = {
                "order": order or "stationcount",
                "reverse": reverse or "false",
                "hidebroken": hidebroken or "true" 
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return response.json()
        except Exception as e:
            return e
    def list_of_states(self, format: str, order: str, reverse: str, hidebroken: str):
        try:
            url = f"{self.base_url}/{format}/states"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            querystring = {
                "order": order or "stationcount",
                "reverse": reverse or "false",
                "hidebroken": hidebroken or "true"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return response.json()
        except Exception as e:
            return e
    def list_of_languages(self, format: str):
        try:
            url = f"{self.base_url}/{format}/languages"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            return response.json()
        except Exception as e:
            return e
    def list_of_tags(self, format: str, filter: str):
        try:
            url = f"{self.base_url}/{format}/languages/{filter}"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            return response.json()
        except Exception as e:
            return e
    def list_of_radio_stations(self, format: str, order: str, reverse: str, offset: str, limit: str, hidebroken: str):
        try:
            url = f"{self.base_url}/{format}/stations"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            querystring = {
                "order": order or "name",
                "reverse": reverse or "false",
                "offset": offset or "0",
                "limit": limit or "10",
                "hidebroken": hidebroken or "true"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return response.json()
        except Exception as e:
            return e
    def list_of_all_radio_stations(self, format: str, order: str, reverse: str, offset: str, limit: str, hidebroken: str):
        try:
            url = f"{self.base_url}/{format}/stations"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            querystring = {
                "order": order or "name",
                "reverse": reverse or "false",
                "offset": offset or "0",
                "limit": limit or "100",
                "hidebroken": hidebroken or "true"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return response.json()
        except Exception as e:
            return e
    def list_of_station_check_results(self, stationuuid: str, lastcheckuuid: str, seconds: str, limit: str):
        try:
            url = f"{self.base_url}/{format}/checks"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            querystring = {
                "stationuuid": stationuuid,
                "lastcheckuuid": lastcheckuuid,
                "seconds": seconds,
                "limit": limit
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return response.json()
        except Exception as e:
            return e
    def list_of_station_clicks(self, stationuuid: str, seconds: str):
        try:
            url = f"{self.base_url}/{format}/clicks"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            querystring = {
                "stationuuid": stationuuid,
                "seconds": seconds
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return response.json()
        except Exception as e:
            return e
    def search_radio_stations_by_uuid(self, format: str, uuid: str):
        try:
            url = f"{self.base_url}/{format}/stations/byuuid"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            querystring = {
                "uuid": uuid
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return response.json()
        except Exception as e:
            return e
    def search_radio_stations_by_url(self, format: str, url: str):
        try:
            url = f"{self.base_url}/stations/byurl"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            querystring = {
                "url": url
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return response.json()
        except Exception as e:
            return e
    def stations_by_clicks(self, format: str, offset: str, limit: str, hidebroken: str, rowcount: str):
        try:
            url = f"{self.base_url}/{format}/stations/topclick/{rowcount}"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            querystring = {
                "offset": offset,
                "limit": limit,
                "hidebroken": hidebroken
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return response.json()
        except Exception as e:
            return e
    def stations_by_votes(self, format: str, offset: str, limit: str, hidebroken: str, rowcount: str):
        try:
            url = f"{self.base_url}/{format}/stations/topvote/{rowcount}"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            querystring = {
                "offset": offset,
                "limit": limit,
                "hidebroken": hidebroken
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return response.json()
        except Exception as e:
            return e
    def station_by_last_click(self, format: str, offset: str, limit: str, hidebroken: str, rowcount: str):
        try:
            url = f"{self.base_url}/{format}/stations/lastclick/{rowcount}"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            querystring = {
                "offset": offset,
                "limit": limit,
                "hidebroken": hidebroken
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return response.json()
        except Exception as e:
            return e
    def vote_for_a_station(self, format: str, uuid: str):
        try:
            url = f"{self.base_url}/{format}/vote/{uuid}"
            headers = {
                'x-rapidapi-host': self.host,
                'x-rapidapi-key': self.api_key
            }
            response = requests.request("GET", url, headers=headers)
            return response.json()
        except Exception as e:
            return e