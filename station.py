import requests
import sys
from tabulate import tabulate
from bs4 import BeautifulSoup


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["1", "2"]:
        sys.exit("Incorrect")
    elif sys.argv[1] == "1":
        table = single()
    else:
        table = multi()
    # Print
    print(tabulate(table, headers=["Title", "Original price", "Discounted price"]))



# Single game
def single():
    # Get the page via requests
    page = requests.get("https://store.playstation.com/en-fi/product/EP4497-CUSA01439_00-0000000000000001")
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


if __name__ == "__main__":
    main()