import re


def all_prices(soup):
    prices = soup.find_all(string=re.compile(r"[$|€|£|\w][0-9]+[\.|,][0-9]+"))

    try:
        text_price = soup.find(
            attrs={"data-qa": "mfeCtaMain#offer1#finalPrice", "data-qa": "mfeCtaMain#offer0#finalPrice"},
            string=re.compile(r"[a-zA-Z]"),
        ).text
    except AttributeError:
        text_price = None

    unique = []
    for price in prices:
        if price.text not in unique and price.text != "":
            unique.append(price.text)
        else:
            continue

    # unique = sorted(unique, key=lambda price: re.search(r"\w+[\.|,]\w+", price).group(0))

    if len(unique) > 1:
        return unique[0], unique[-1]
    elif text_price != None:
        return text_price, unique[0]
    else:
        return None, unique[0]
