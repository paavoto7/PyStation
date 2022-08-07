# **PyStation**

PyStation is a Playstation Store crawler that lets the users to gather information about a specific game or discounted games.  

The results can be either printed on the command line or displayed on the screen including the games image.

**Current Features**
- Title
- Price (Discounted available only for the sales)
- Image (If used the gui option)

## **Usage**
    python3 -m pystation [options] [args]
    Or
    python3 pystation-runner.py [options] [args]

PyStation is run using the command line.  
Run -h as option to see the full usage

**Programmable Search Engine**  

To create your own Googles programmable search engine: https://developers.google.com/custom-search/v1/overview
  
The site to search is: **store.playstation.com/*** <sub>The star representing all subdomains</sub>  
The reason everyone has to create their own, is that the free version only has 100 free queries per day.  
After creating one, you should be able to get the key and the ID/cx and then paste them into the constants.py file:

    key=...
    cx=...

### **A few notes about the implementations**

First I was only going to do CLI but as the project went on it expanded to GUI as well. Tkinter was chosen as it is the easiest option to develop GUI features on Python.  

All external library dependancies were chosen for their ease and fit for the project. Usage of too sophisticated libraries would've been waste of time.

Google has also created a [python library for the programmable search engine](https://github.com/googleapis/google-api-python-client). I decided to not use it but the code shouldn't be too hard to modify it felt like it.