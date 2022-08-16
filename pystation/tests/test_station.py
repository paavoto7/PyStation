import re
import sys

import pytest

from ..cli.cli import main
from ..search.highest_price import all_prices
from ..search.search_funcs import search_store
from ..station import multi, single

"""Regex is used here because the country and language are not necessarily the same for all users.
The title and the price especially may also differ so anything hardcoded won't do here."""


# This is to test the whole working of the cli
@pytest.mark.parametrize("option, game", [("-s", "ezio"), ("-s", "witcher")])
def test_whole(capsys, monkeypatch, option, game):
    with monkeypatch.context() as m:
        m.setattr(sys, "argv", ["pystation/__main__.py", option, game])
        main()
        captured = capsys.readouterr().out
        assert "Original price" in captured and game in captured.lower()


def test_single():
    title, price = single("minecraft")[0]
    assert re.search(r"\w*Minecraft\w*", title)
    assert re.search(r"\D+\d+[,|.]\d+", price)


def test_multi():
    assert len(multi()) > 1
    assert type(multi()[3][0]) == str


def test_invalid_game():
    with pytest.raises(SystemExit):
        single("halo")
