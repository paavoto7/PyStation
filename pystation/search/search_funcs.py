import re
import sys

import requests
from bs4 import BeautifulSoup


# Get the latest sale
def search_store(url):
    # Pass a user agent so the server will serve the proper site
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
    # Create soup object
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")

    # Assure that the search wasn't empty
    if soup.find("div", attrs={"data-qa": "search-no-results"}):
        sys.exit("No search results found. Try specifying the search query.")

    #
    return soup
    # Return f-string containg the url for the sale


# Check that the search result is a game
def search_game(url):
    soup = search_store(url)
    game_tags = soup.find_all("a", class_="psw-link psw-content-link")
    for i in range(len(game_tags)):
        if not (
            tag := game_tags[i].find(
                "span",
                class_="psw-product-tile__product-type psw-t-bold psw-t-size-1 psw-t-truncate-1 psw-c-t-2 psw-t-uppercase psw-m-b-1",
                attrs={
                    f"'data-qa':'{re.compile(r'search#productTile[0-9]{2}#product-type')}'"
                },
            )
        ) or tag.string in ["Pre-Order", "Game Bundle"]:
            return f"https://store.playstation.com{game_tags[i].get('href')}"
        else:
            continue

    sys.exit("Page seems to be invalid. Try specifying the search query.")


def search_deal(url):
    soup = search_store(url)
    href = soup.find(
        "a",
        class_="psw-link psw-quick-action-link psw-button psw-b-0 psw-t-button psw-l-line-center psw-button-sizing psw-button-sizing--medium psw-button-sizing--icon-only psw-quick-action-button",
    ).get("href")
    return f"https://store.playstation.com{href}"
