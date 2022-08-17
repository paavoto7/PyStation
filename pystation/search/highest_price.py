import re


def all_prices(soup):
    prices = soup.find_all(string=re.compile(r"\D*[0-9]+[\.|,][0-9]+"))

    offer_price = offer(soup)

    unique = []
    for price in prices:
        if price.text not in unique and price.text != "":
            unique.append(price.text)
        else:
            continue

    if len(unique) > 1:
        unique = sorted(
            unique, key=lambda price: re.search(r"\w+[\.|,]\w+", price).group(0)
        )
        return unique[0], unique[-1]

    elif offer_price != None and offer_price not in unique:
        if len(unique) > 0:
            return offer_price, unique[0]
        else:
            return offer_price, None

    else:
        return None, unique[0]


def offer(soup):
    try:
        offer_price = soup.find(
            attrs={"data-qa": "mfeCtaMain#offer1#finalPrice"},
        ).string
    except AttributeError:
        try:
            offer_price = soup.find(
                attrs={"data-qa": "mfeCtaMain#offer0#finalPrice"},
            ).string
        except AttributeError:
            return None

    try:
        condition = soup.find(
            "span",
            string=re.compile(r"[+]*PlayStation[+]*"),
            attrs={"data-qa": re.compile(r"mfeCtaMain#offer[0-9]+#discountInfo")},
        ).string
    except AttributeError:
        condition = ""

    if tier := re.search(r"(Premium|Extra)", condition):
        return f"{offer_price} with PlayStation Plus {tier.group(0)}"

    elif "PlayStation Plus" in condition:
        return f"{offer_price} with PlayStation Plus"

    else:
        return offer_price
