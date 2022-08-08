import argparse
import re
import sys

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

from .gui import station_gui as gui
from .search.search_funcs import search_google, search_sale

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
