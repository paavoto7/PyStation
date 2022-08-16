import inspect
import io
import re
import sys
from tkinter import *

import requests
from PIL import Image, ImageTk


# Make a class in order to scale
class Game:
    def __init__(self, image, price, full_title):
        img = Image.open(io.BytesIO(image))
        # Get the measurements
        width, height = img.size
        # Resize the image to not take the whole screen
        img = img.resize((int(width / 1.3), int(height / 1.3)))

        # Assign the image, price and the title
        self.image = ImageTk.PhotoImage(img)
        self.price = price
        self.full_title = full_title

    def get(self):
        return vars(self)


# Make a class for the navigations
class Navs:
    def __init__(self, max_iter):
        # Iterator to keep track over the current image
        self._iterator = 0
        # to define how far can the the images be iterated
        self.max_iter = max_iter

    @property
    def iterator(self):
        return self._iterator

    @iterator.setter
    def iterator(self, oper):
        # Check whether the iterator would go beyond the boundaries
        if 0 <= self._iterator + oper <= self.max_iter:
            self._iterator = self._iterator + oper
        else:
            pass

    def next_img(self, event, games):
        self.iterator = 1
        game = games[self.iterator]
        img = game.image
        event.config(image=img, text=f"{game.full_title}: {game.price}")
        event.image = img

    def previous_img(self, event, games):
        self.iterator = -1
        game = games[self.iterator]
        img = game.image
        event.config(image=img, text=f"{game.full_title}: {game.price}")
        event.image = img


# Start the gui and check where the function call came from
def main_app(*args):
    root = Tk()
    if inspect.stack()[1][3] == "single":
        Display(root, *args)
        root.mainloop()

    elif inspect.stack()[1][3] == "main":
        Multi_display(root, *args)
        root.mainloop()
    else:
        sys.exit("Invalid function call.")


# Single game display
class Display:
    def __init__(self, master, url, price, full_title):
        self.master = master

        self.game = Game(self.image(url), price, full_title)

        master.title("Game")

        imagelab = Label(
            master,
            image=self.game.image,
            text=f"{full_title}: {price}",
            compound=BOTTOM,
        )
        imagelab.img = self.game.image
        imagelab.config(font=("Times", 25, "bold italic"))
        imagelab.grid(row=0, column=0)

    def image(self, url):
        # Change the image width to 1920 and thumbnail false in the url
        new_url = url.replace(
            str(re.search(r"w=[0-9]+\&thumb=true", url).group()),
            "w=1920&thumb=false",
        )
        # Get the image
        return requests.get(new_url).content


# Discountd games display
class Multi_display:
    def __init__(self, master, table):

        games = list()
        for game in table[0:]:
            img = requests.get(game[3]).content
            games.append(Game(img, game[1], game[0]))

        # Assign a title
        master.title("Discounted Games")

        imagelab = Label(
            master,
            image=games[0].image,
            text=f"{games[0].full_title}: {games[0].price}",
            compound=BOTTOM,
        )
        imagelab.config(font=("Times", 25, "bold italic"))
        imagelab.pack(fill=BOTH, expand=True)

        # Create a Navs object
        navs = Navs(len(games) - 1)

        btnfr = Button(
            master, text="Next Game", command=lambda: navs.next_img(imagelab, games)
        )
        btnfr.pack(side=RIGHT)

        btnpr = Button(
            master,
            text="Previous Game",
            command=lambda: navs.previous_img(imagelab, games),
        )
        btnpr.pack(side=LEFT)
