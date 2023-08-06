from typing import *

import requests


class PandaScoreAPIClient:
    def __init__(self, API_KEY: str = "", settings: dict = {}):
        if API_KEY != "":
            self.API_KEY = API_KEY

            self.headers = {
                "Accept": "application/json",
                "Authorization": "Bearer " + self.API_KEY,
            }

        if settings != {}:
            self.settings = settings

        self.base_urls = {
            "incidents": "https://api.pandascore.co/additions",
            "leagues": "https://api.pandascore.co/leagues",
            "lives": "https://api.pandascore.co/lives",
            "matches": "https://api.pandascore.co/matches",
            "players": "https://api.pandascore.co/players",
            "series": "https://api.pandascore.co/series",
            "teams": "https://api.pandascore.co/teams",
            "tournaments": "https://api.pandascore.co/tournaments",
            "videogames": "https://api.pandascore.co/videogames",
        }

    def get_request(self, url: str) -> requests.Response:

        if "filter" in self.settings:
            if self.settings["filter"]["enabled"]:
                url = self.apply_filter(url)

        if "search" in self.settings:
            if self.settings["search"]["enabled"]:
                url = self.apply_search(url)

        if "range" in self.settings:
            if self.settings["range"]["enabled"]:
                url = self.apply_range(url)

        if "sorting" in self.settings:
            if self.settings["sorting"]["enabled"]:
                url = self.apply_sorting(url)

        if "pagination" in self.settings:
            if self.settings["pagination"]["enabled"]:
                url = self.apply_pagination(url)

        response = requests.request("GET", url, headers=self.headers)
        return response

    def set_filter(self, settings: dict) -> None:
        self.settings["filter"] = settings

    def set_search(self, settings: dict) -> None:
        self.settings["search"] = settings

    def set_range(self, settings: dict) -> None:
        self.settings["range"] = settings

    def set_sorting(self, settings: dict) -> None:
        self.settings["sorting"] = settings

    def set_pagination(self, settings: dict) -> None:
        self.settings["pagination"] = settings

    def apply_filter(self, url: str) -> str:
        return url

    def apply_search(self, url: str) -> str:
        return url

    def apply_range(self, url: str) -> str:
        return url

    def apply_sorting(self, url: str) -> str:
        return url

    def apply_pagination(self, url: str) -> str:
        return url

    def list_leagues(self) -> List:
        url = self.base_urls["leagues"]
        response = self.get_request(url)

        return response.json()

    def get_league(self, id: int, slug: str):
        url = self.base_urls["leagues"]

        if id:
            url += str(id)
        elif slug:
            url += slug
        else:
            raise Exception("Something went wrong")

        response = self.get_request(url)
        return response.json()
