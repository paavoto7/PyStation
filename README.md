# **PyStation**

PyStation is a Playstation Store crawler that lets the users to gather information about a specific game or a number of discounted games.  

The results can either be printed on the command line or displayed on the screen with addition of the games images.

**Current Features**
- Title
- Price (Discounted price only available for the multi options)
- Image (Only on the gui option)

**Possible Future Development**  
- Description
- Multiple single game searches
- Better code organization
- Publishing this as an API to PYPI

## **Usage**
    python3 -m pystation [options] [args]
    Or
    python3 pystation-runner.py [options] [args]

PyStation is used from the command line.  
Run -h as option to see the full usage.

**Programmable Search Engine**  

To create your own Google's programmable search engine, refer to this site: https://developers.google.com/custom-search/v1/overview
  
While creating the engine, the site to search is: **store.playstation.com/*** <sub>The star representing all subdomains</sub>  
The reason everyone has to create their own engine is that the free version only has 100 free queries per day.  
After creating one, you should be able to get the key and the ID/cx and then paste them into the constants.py file:

    key=...
    cx=...

Or alternatively you could create environmental variables:

    export API_KEY=...
    export CX=...

### **A few notes about the implementations**

First I was only going to do CLI but as the project went on, I decided to expand to GUI as well. Tkinter was chosen there as it is the easiest option to develop GUI features on Python.  

All external library dependancies were chosen for their ease and fit for the project. Usage of too sophisticated libraries would've been a waste of time and resources.

Google has also created a [python library for the programmable search engine](https://github.com/googleapis/google-api-python-client). I decided not to use it but the code shouldn't be too hard to modify if felt like it.