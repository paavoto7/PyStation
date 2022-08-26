import re
import sys

import requests
from bs4 import BeautifulSoup

from pystation.gui import station_gui as gui
from pystation.search.highest_price import all_prices
from pystation.search.search_funcs import search_deal, search_game


# Single game
def single(title, country="en-us", use_gui=None):
    url = f"https://store.playstation.com/{country}/search/{title}"
    # Get the page via requests
    page = requests.get(search_game(url))
    # Create the soup object
    soup = BeautifulSoup(page.content, "html.parser")

    # Search the lowest and highest price
    try:
        disc, price = all_prices(
            soup.find(
                class_="psw-c-bg-card-1 psw-p-y-7 psw-p-x-8 psw-m-sub-x-8 psw-m-sub-x-6@below-tablet-s psw-p-x-6@below-tablet-s"
            )
        )
    except AttributeError:
        sys.exit("The page seems to be invalid. Try specifying the search query.")

    # Add the items to a list in order to use list comprehension later
    items = [soup.find("h1").string, price, disc]

    # If gui is provided
    if use_gui == True:
        # Get image
        image = soup.find(
            "img", class_="psw-blur psw-right-top-third psw-l-fit-cover"
        ).get("src")

        # Display the image
        return gui.main_app(image, price, items[0])

    # Populate the list using list comprehension. Reverse because title is appended after.
    return [[item for item in items if item != None]]


# Sale
def multi(country="en-us", use_gui=None):
    search_url = f"https://store.playstation.com/{country}/pages/deals"
    # Get the page via requests
    page = requests.get(search_deal(search_url))
    # Create the soup object
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        # Get the original price of the game
        discprice = soup.find_all("span", class_="psw-m-r-3")
        # Get the discounted price of the game
        ogprice = soup.find_all(lambda tag: tag.get("class") == ["psw-c-t-2"])
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
