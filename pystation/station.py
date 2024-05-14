import re
import sys

import requests
from bs4 import BeautifulSoup

from pystation.search.highest_price import all_prices
from pystation.search.search_funcs import search_deal, search_game


# Single game
def single(title, country="en-us"):
    url = f"https://store.playstation.com/{country}/search/{title}"
    # Get the page via requests
    page = requests.get(search_game(url))
    # Create the soup object
    soup = BeautifulSoup(page.content, "html.parser")

    # Search the lowest and highest price
    try:
        disc, price = all_prices(
            soup.find(
                class_="psw-l-line-left psw-l-line-wrap"
            )
        )
    except AttributeError:
        sys.exit("The page seems to be invalid. Try specifying the search query.")

    # Add the items to a list in order to use list comprehension later
    items = [soup.find("h1").string, price, disc]

    # Populate the list using list comprehension. Reverse because title is appended after.
    return [[item for item in items if item != None]]


# Sale
def multi(country="en-us"):
    #search_url = f"https://store.playstation.com/{country}/pages/deals"
    search_url = "https://store.playstation.com/en-fi/pages/latest"
    # Get the page via requests
    page = requests.get(search_deal(search_url))
    # Create the soup object
    soup = BeautifulSoup(page.content, "html.parser")
    with open("./moi.html", "w") as m:
        m.write(str(page.content))

    try:
        games = soup.find(attrs={"data-qa": "ems-sdk-strand#viewMore#tabletAndAbove"})
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
    # Append the information to the list
    for i in range(len(title)):
        table.append([title[i].text, ogprice[i].text, discprice[i].text])
    return table
