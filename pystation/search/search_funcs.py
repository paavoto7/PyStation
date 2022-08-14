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
    href = search_game(soup.find_all("a", class_="psw-link psw-content-link"))
    # Return f-string containg the url for the sale
    return f"https://store.playstation.com{href}"


def search_game(game_tags, i=0):
    if not (
        tag := game_tags[i].find(
            "span",
            class_="psw-product-tile__product-type psw-t-bold psw-t-size-1 psw-t-truncate-1 psw-c-t-2 psw-t-uppercase psw-m-b-1",
            attrs={
                f"'data-qa':'{re.compile(r'search#productTile[0-9]{2}#product-type')}'"
            },
        )
    ) or tag.string in ["Pre-Order", "Game Bundle"]:
        return f"{game_tags[i].get('href')}"
    else:
        return search_game(game_tags, i + 1)
