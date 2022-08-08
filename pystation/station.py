from .gui import station_gui as gui
import requests
import sys
from tabulate import tabulate
from bs4 import BeautifulSoup
import urllib.parse as urlparse
import argparse
import re

# Import the API key and Programmable search engine ID
from .constants import key, cx

"""This file contains all the necessary functions for the script to be working.
Main handles the argument parsing of the command line arguments.
THe functions could be split into multiple files, but that is for the future for now at least.
"""


def main():
    parser = argparse.ArgumentParser(description="Playstation Store price crawler")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-s",
        "--single",
        help="Get a single game price and information.",
        type=str,
        nargs="+",
    )
    group.add_argument(
        "-gs",
        "--gui_single",
        help="Same as single but with gui and picture",
        type=str,
        nargs="+",
    )
    group.add_argument(
        "-m", "--multi", help="Get all the sale prices and titles", action="store_true"
    )
    group.add_argument(
        "-gm",
        "--gui_multi",
        help="Same as multi but with gui and picture",
        action="store_true",
    )

    args = parser.parse_args()

    if args.single:
        table = single(args.single)
    elif args.gui_single:
        table = single(args.gui_single, True)
        sys.exit(0)
    elif args.gui_multi:
        table = gui.multi_display(multi(True))
        sys.exit(0)
    elif args.multi:
        table = multi()
    else:
        sys.exit("Something went wrong. Refer to the help.")
    # Print
    print(tabulate(table, headers=["Title", "Original price", "Discounted price"]))


# Single game
def single(title, use_gui=None):
    # Get the page via requests
    page = requests.get(search_google(title))
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
    # Get the page via requests
    page = requests.get(search_sale())
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
    # Return the url of the Playstation Store
    return result["items"][0]["link"]