import requests
from utils.config import OMDB_API_KEY
from utils.config import API_BASE_URL
from cachetools import TTLCache


class OMDBClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.api_key = OMDB_API_KEY
        self.cache = TTLCache(maxsize=100, ttl=3600)

    def search_movies(self, query):
        endpoint = f"{self.base_url}"
        params = {"apikey": self.api_key, "s": query}
        response = requests.get(endpoint, params=params)

        return response.json().get("Search", [])

    def retrieve_movie_info(self, imdb_id):
        if imdb_id in self.cache:
            return self.cache[imdb_id]
        
        endpoint = f"{self.base_url}"
        params = {"apikey": self.api_key, "i": imdb_id, "plot": "full"}
        response = requests.get(endpoint, params=params)

        response_data = response.json()
        self.cache[imdb_id] = response_data

        return response_data

