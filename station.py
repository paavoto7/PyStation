import requests
import sys
from tabulate import tabulate
from bs4 import BeautifulSoup
import urllib.parse as urlparse


def main():
    if sys.argv[1] not in ["--s", "--m"]:
        sys.exit("Incorrect command line argument")
    elif sys.argv[1] == "--s":
        table = single(sys.argv[2])
    else:
        table = multi()
    # Print
    print(tabulate(table, headers=["Title", "Original price", "Discounted price"]))



# Single game
def single(title):
    # Get the page via requests
    page = requests.get(search_google(title))
    # Create the soup object
    soup = BeautifulSoup(page.content, "html.parser")

    # Find the price
    price = soup.find("span", class_="psw-t-title-m").string
    # Find the title
    title = soup.find("h1").string
    # Make table
    return [[title, price]]


# Sale 
def multi():
    # Get the page via requests
    page = requests.get(search_sale("https://store.playstation.com/en-fi/pages/latest"))
    # Create the soup object
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the original price of the game
    ogprice = soup.find_all("span", class_="psw-m-r-3")
    # Get the discounted price of the game
    discprice = soup.find_all(lambda tag: tag.get("class") == ["psw-c-t-2"])
    # Get the title of the game
    title = soup.find_all("span", class_="psw-t-body psw-c-t-1 psw-t-truncate-2 psw-m-b-2")

    table = []
    # Append the information to the list
    for i in range(len(title)):
        table.append([title[i].text, ogprice[i].text, discprice[i].text])
    return table


# Get the latest sale
def search_sale(url):
    # Create soup object
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    # Return f-string containg the url for the sale
    return f'https://store.playstation.com{soup.find("a", class_="psw-link psw-content-link").get("href")}'


# Search Googles programmable search engine
def search_google(title):
    # Base url
    api_url = "https://www.googleapis.com/customsearch/v1"
    # The search parameters
    params = {
        "key": "Insert API key here",
        "cx": "Insert Search engine ID here",
        "q": title
    }

    # Split the url into parts using urllib.parse
    url_parts = list(urlparse.urlparse(api_url))
    # Change the parameters field
    url_parts[4] = urlparse.urlencode(params)

    # Construct the final url
    final_url = urlparse.urlunparse(url_parts)
    # 
    data = requests.get(final_url).json()
    return data["items"][0]["link"]


if __name__ == "__main__":
    main()