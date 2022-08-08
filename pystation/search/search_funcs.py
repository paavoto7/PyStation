import os
import sys
import urllib.parse as urlparse

import requests
from bs4 import BeautifulSoup

# Import the API key and Programmable search engine ID
try:
    # Try if environmental variables set
    key = os.environ["API_KEY"]
    cx = os.environ["CX"]
except KeyError:
    # If no env variables, try to import from constants
    try:
        from ..constants import cx, key
    except ModuleNotFoundError:
        sys.exit("Neither environmental variables nor the constants.py file found.")


# Get the latest sale
def search_sale():
    url = "https://store.playstation.com/en-fi/pages/deals"
    # Create soup object
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    # Return f-string containg the url for the sale
    return f'https://store.playstation.com{soup.find("a", class_="psw-link psw-content-link").get("href")}'


# Search Googles programmable search engine
def search_google(title):
    # Base url for the api
    api_url = "https://www.googleapis.com/customsearch/v1"
    # The search parameters
    params = {"key": key, "cx": cx, "lr": "lang_fi", "q": title}

    # Split the url into parts using urllib.parse
    url_parts = list(urlparse.urlparse(api_url))
    # Change the parameters field
    url_parts[4] = urlparse.urlencode(params)

    # Construct the final url
    final_url = urlparse.urlunparse(url_parts)
    # Get the search results
    result = requests.get(final_url).json()

    # If error happened in the search
    if "error" in result:
        sys.exit(f"{result['error']['message']} Refer to the README.")

    # Return the url of the Playstation Store
    return result["items"][0]["link"]
