import re
import sys

import requests
from bs4 import BeautifulSoup

from .gui import station_gui as gui
from .search.search_funcs import search_store

"""This file contains all the necessary functions for the script to be working.
"""


# Single game
def single(title, currency="us", use_gui=None):
    url = f"https://store.playstation.com/en-{currency}/search/{title}"
    # Get the page via requests
    page = requests.get(search_store(url))
    # Create the soup object
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        # Find the price
        price = soup.find("span", class_="psw-t-title-m").string
        # Find the title
        full_title = soup.find("h1").string
    except AttributeError:
        sys.exit("The page seems to be invalid. Try specifying the search query.")

    # If gui is provided
    if use_gui == True:
        # Get image
        image = soup.find(
            "img", class_="psw-blur psw-right-top-third psw-l-fit-cover"
        ).get("src")
        # Display the image
        return gui.display(image, price, full_title)
    # Make table
    return [[full_title, price]]


# Sale
def multi(use_gui=None):
    search_url = "https://store.playstation.com/en-us/pages/deals"
    # Get the page via requests
    page = requests.get(search_store(search_url))
    # Create the soup object
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        # Get the original price of the game
        ogprice = soup.find_all("span", class_="psw-m-r-3")
        # Get the discounted price of the game
        discprice = soup.find_all(lambda tag: tag.get("class") == ["psw-c-t-2"])
        # Get the title of the game
        title = soup.find_all(
            "span", class_="psw-t-body psw-c-t-1 psw-t-truncate-2 psw-m-b-2"
        )
    except AttributeError:
        sys.exit("The page seems to be invalid.")

    table = []

    if use_gui == True:
        image = soup.find_all("img", class_="psw-blur psw-top-left psw-l-fit-cover")
        for i in range(len(title)):
            url = image[i]["src"].replace(
                str(re.search(r"w=[0-9]+\&thumb=true", image[i]["src"]).group()),
                "w=1920&thumb=false",
            )
            table.append([title[i].text, ogprice[i].text, discprice[i].text, url])
        return table

    else:
        # Append the information to the list
        for i in range(len(title)):
            table.append([title[i].text, ogprice[i].text, discprice[i].text])
        return table
