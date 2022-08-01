from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import io
import requests
import re


# Make a class in order to scale
class Game:
    def __init__(self, image, price, full_title):
        try:
            img = Image.open(io.BytesIO(image)).resize((1500, 844))
            self.image = ImageTk.PhotoImage(img)
        except:
            self.image = image
        self.price = price
        self.full_title = full_title

    def get(self):
        return vars(self)


# Make a class for the navigations
class Navs:
    def __init__(self, max_iter):
        self._iterator = 0
        self.max_iter = max_iter
    
    @property
    def iterator(self):
        return self._iterator

    @iterator.setter
    def iterator(self, oper):
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
    new_url = url.replace(str(re.search(r"w=[1-9]+\&thumb=true", url).group()), "w=1920thumb=false")
    # Get the image
    image = requests.get(new_url).content
    
    # Create the Tk object
    root = Tk()
    # Assign a title
    root.title("Games")
    # Create the Game object
    img = Game(image, price, full_title).image
    
    imagelab = Label(root, image=img, text=f"{full_title}: {price}", compound=BOTTOM)
    imagelab.config(font=("Times", 25, "bold italic"))
    imagelab.grid(row=0, column=0)

    #root.geometry(f"{width}x{height}+0+0")
    #root.attributes("-zoomed", True)
    return root.mainloop()


def multi_display(table):
    root = Tk()
    games = list()
    for game in table[0:]:
        url = requests.get(game[3]).content
        games.append(Game(url, game[1], game[0]))

    # Assign a title
    root.title("Games")

    imagelab = Label(root, image=games[0].image, text=f"{games[0].full_title}: {games[0].price}", compound=BOTTOM)
    imagelab.config(font=("Times", 25, "bold italic"))
    imagelab.pack(fill=BOTH, expand=True)

    # Create a Navs object
    navs = Navs(len(games) - 1)

    btnfr = Button(root, text="Next Image", command = lambda: navs.next_img(imagelab, games))
    btnfr.pack(side=LEFT)

    btnpr = Button(root, text="Previous Image", command = lambda: navs.previous_img(imagelab, games))
    btnpr.pack(side=RIGHT)

    return root.mainloop()
