import io
import re
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


def display(url, price, full_title):
    # Change the image width to 1920 and thumbnail false in the url
    new_url = url.replace(
        str(re.search(r"w=[0-9]+\&thumb=[true|false]", url).group()),
        "w=1920&thumb=false",
    )
    # Get the image
    image = requests.get(new_url).content

    # Create the Tk object
    root = Tk()
    # Assign a title
    root.title("Game")
    # Create the Game object
    img = Game(image, price, full_title).image

    imagelab = Label(root, image=img, text=f"{full_title}: {price}", compound=BOTTOM)
    imagelab.config(font=("Times", 25, "bold italic"))
    imagelab.grid(row=0, column=0)

    return root.mainloop()


def multi_display(table):
    root = Tk()
    games = list()
    for game in table[0:]:
        img = requests.get(game[3]).content
        games.append(Game(img, game[1], game[0]))

    # Assign a title
    root.title("Discounted Games")

    imagelab = Label(
        root,
        image=games[0].image,
        text=f"{games[0].full_title}: {games[0].price}",
        compound=BOTTOM,
    )
    imagelab.config(font=("Times", 25, "bold italic"))
    imagelab.pack(fill=BOTH, expand=True)

    # Create a Navs object
    navs = Navs(len(games) - 1)

    btnfr = Button(
        root, text="Next Game", command=lambda: navs.next_img(imagelab, games)
    )
    btnfr.pack(side=RIGHT)

    btnpr = Button(
        root, text="Previous Game", command=lambda: navs.previous_img(imagelab, games)
    )
    btnpr.pack(side=LEFT)

    return root.mainloop()
