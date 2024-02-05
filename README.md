**!! As of now, some things are broken and don't seem to work as expected. Will be fixed when enough free time is available.**
# **PyStation**

PyStation is a Playstation Store crawler that lets the users to gather information about a specific game or a number of discounted games.  

PyStation can either be used as a command line tool or an API.
The CLI results can either be printed on the command line or displayed on the screen with addition of the games images.

## **Installation**
**!! The package on PyPI doesn't have the updated requirements**

    pip install PyPlayStation

The name of the PyPI project is different because the name *PyStation* was already taken.

Forking the project is always an option too.

## **Current Features**
- Title
- Price (Discounted price only available for the multi options)
- Image (Only on the gui option)

**Possible Future Development**  
- Description and Publisher of the game
- Multiple single game searches
- Better code organization
- Publishing as a CLI tool and API to PYPI
- Improve the gui
    - Main menu
    - More beautiful interface
    - etc. 

## **CLI Tool Usage**

    pystation [options] [args]

    Options:

    -h, --help            show this help message and exit
    -s SINGLE [SINGLE ...], --single SINGLE [SINGLE ...]
                            Get a single game price and information.
    -gs GUI_SINGLE [GUI_SINGLE ...], --gui_single GUI_SINGLE [GUI_SINGLE ...]
                            Same as single but with gui and picture
    -m, --multi           Get all the sale prices and titles
    -gm, --gui_multi      Same as multi but with gui and picture

Using the gui feature doesn't have any other benefit than seeing the images.

In order to get your desired currency for the prices, you need to specify the country.  
It is specified by adding **-c country** after the options and args.  

    For e.g.
    pystation -s minecraft -c germany

Some languages that don't use letters may have unexpectable behavior as the text capturing is done for lating alphabets.

## **API Usage**

The *single* and *multi* functions in the station.py file are the most useful as the other ones are mainly helpers for these two.  
The country here is just any country name e.g. Finland.

    from pystation.station import single, multi
    single(title, [country]) -> [[full title, price]]
    multi([country]) -> [[full title, og price, discounted price] * x]


### **A few notes about the implementations**

First I was only going to do CLI but as the project went on, I decided to expand to GUI as well. Tkinter was chosen there as it is the easiest option to develop GUI features on Python.  

All external library dependancies were chosen for their ease and fit for the project. Usage of too sophisticated libraries would've been a waste of time and resources.

Both the single and the multi funtion uses the search_store function.
It's unnecessary for the multi to be checked for no results or be passed through the search_game function.
It is made this way as it doesn't add too much time and saves a few lines of redundant code.

All files are formatted using black.
