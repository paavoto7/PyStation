from pystation.station import single, multi, search_google, search_sale
import pytest


def test_single():
    assert single("stray") == [["Stray", "€29,95"]]


def test_multi():
    assert len(multi()) > 1


def test_google():
    assert search_google("ezio") == "https://store.playstation.com/fi-fi/product/EP0001-CUSA04893_00-ACLEGACYHD000000"


def test_sale():
    assert len(search_sale()) > 1 


def test_invalid_game():
    with pytest.raises(SystemExit):
        single("fifa 08")